import time
from datetime import datetime, timedelta

from discord.ext import commands
from discord.ext.commands import BadArgument, MissingRequiredArgument

import faucet
import secrets
import user_db
from faucet import valid_address

from logger import log

disc_token = secrets.DISCORD_TOKEN

prefix = '$'
bot = commands.Bot(command_prefix=prefix)


# ADMIN_DISCORD_ROLES = ()


@bot.event
async def on_ready():
    log(f'Logged in as {bot.user} (ID: {bot.user.id})')
    log('--------')


@bot.command(name='version', help='usage: ' + prefix + 'version')
async def faucet_version(ctx):
    print("here")
    await ctx.send('v1.0.0')


@bot.command(name='testnet', help='usage: ' + prefix + 'testnet [address]')
async def testnet_faucet(ctx, address: str):
    print(ctx.channel.id)
    if int(ctx.channel.id) != int(961609330501763072) and int(ctx.channel.id) != int(967597663535120384):
        await ctx.send("Please only use the <#961609330501763072> channel.")
        return
    if "comdex1" in address:
        chain = "comdex"
        token = "CMDX"
        tokens_requested = secrets.MAX_COMDEX_TESTNET_TOKENS_REQUESTED
    elif "cosmos1" in address:
        chain = "cosmos"
        token = "ATOM"
        tokens_requested = secrets.MAX_COSMOS_TESTNET_TOKENS_REQUESTED
        # await ctx.send("Cosmos is not supported yet.")
        # return
    elif "osmo1" in address:
        chain = "osmo"
        token = "OSMO"
        tokens_requested = secrets.MAX_OSMOSIS_TESTNET_TOKENS_REQUESTED
        # await ctx.send("Please use `https://faucet.osmosis.zone` for OSMO tokens.")
        # return
    else:
        await ctx.send("This chain is not supported.")
        return

    db_connection = user_db.get_db_connection()

    # if the faucet ran out of tokens, deny
    if faucet.get_faucet_balance(chain, "testnet", ctx.guild.id) < tokens_requested:
        response = "The faucet does not have enough funds. More funds are needed at address: `" \
                   + secrets.get_faucet_address(chain, ctx.guild.id) + "`."

    # if the user or address has already received > max Matic, deny
    # elif faucet.get$testnet comdex1vgenpdplmlwvmn2kks4h2784ezt8pgup7pqsn5_address_balance(chain, "testnet", address) >= MAX_TOKENS_REQUESTED:
    #    response = "You have over " + str(MAX_TOKENS_REQUESTED) + token + " in your wallet. Please request more when you run out."

    # if the user has requested in the past 24 hours, deny
    elif datetime.now() - datetime.strptime(user_db.get_user_last_transaction_time(db_connection, ctx.author.id, chain, ctx.guild.id), "%m/%d/%Y, %H:%M:%S") < timedelta(hours=24)\
            and not ctx.author.id == 712863455467667526:
        time_diff = datetime.now() - datetime.strptime(user_db.get_user_last_transaction_time(db_connection, ctx.author.id, chain, ctx.guild.id), "%m/%d/%Y, %H:%M:%S")
        response = f"You have already requested. Please request again in: {round((timedelta(days=1)-time_diff).seconds/3600, 2)} hours."

    # if the address is not valid, deny
    elif not valid_address(address):
        response = "usage: `" + prefix + "testnet [address]`. \n" \
                                         "Please enter a valid address."

    # if we passed all the above checks, proceed
    else:
        resp = faucet.send_transaction(chain, "testnet", address, tokens_requested, ctx.guild.id)

        # success = True
        if len(resp) == 64:
            user_db.add_transaction(db_connection, str(ctx.author.id), datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), chain, ctx.guild.id)
            response = f"Sending {str(tokens_requested)} {token} to {address[:8]}...{address[-4:]}.\nHash: {resp}"
            # time.sleep(1)
        else:
            response = resp

    log("testnet-faucet: " + response)
    await ctx.send(response)
    db_connection.close()
    return


@testnet_faucet.error
async def testnet_faucet_error(ctx, error):
    if isinstance(error, BadArgument):
        await ctx.send("usage: `" + prefix + "testnet [address]`. \n"
                                             "Invalid address.")
        raise error
    elif isinstance(error, MissingRequiredArgument):
        await ctx.send("usage: `" + prefix + "testnet [address]`")
        raise error
    else:
        await ctx.send("Please try again soon. cc:<@712863455467667526>")
        log(error)
        raise error


@bot.command(name='balance', help='usage: ' + prefix + 'balance')
# @commands.has_any_role(*ADMIN_DISCORD_ROLES)
async def get_testnet_balance(ctx):
    try:
        cmdx_balance = faucet.get_faucet_balance("comdex", "testnet", ctx.guild.id)
        osmo_balance = faucet.get_faucet_balance("osmo", "testnet", ctx.guild.id)
        atom_balance = faucet.get_faucet_balance("cosmos", "testnet", ctx.guild.id)
        response = f"The faucet has the following tokens remaining: \n" \
                   f"\t{cmdx_balance} CMDX\n" \
                   f"\t{osmo_balance} OSMO\n" \
                   f"\t{atom_balance} ATOM"
        await ctx.send(response)
    except Exception as e:
        log(e)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


bot.run(disc_token)
