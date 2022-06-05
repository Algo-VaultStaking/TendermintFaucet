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
    await ctx.send('v1.0.0')


@bot.command(name='testnet', help='usage: ' + prefix + 'testnet [address]')
async def testnet_faucet(ctx, address: str):
    if "comdex1" in address:
        chain = "comdex"
        token = "CMDX"
        tokens_requested = secrets.MAX_COMDEX_TESTNET_TOKENS_REQUESTED
    elif "cosmos1" in address:
        chain = "cosmos"
        token = "ATOM"
        tokens_requested = secrets.MAX_COSMOS_TESTNET_TOKENS_REQUESTED
    elif "osmo1" in address:
        chain = "osmo"
        token = "OSMO"
        tokens_requested = secrets.MAX_OSMOSIS_TESTNET_TOKENS_REQUESTED
    else:
        await ctx.send("This chain is not supported.")
        return

    # if the faucet ran out of tokens, deny
    if faucet.get_faucet_balance(chain, "testnet", ctx.guild.id) < tokens_requested:
        response = "The faucet does not have enough funds. More funds are needed at address: `" \
                   + secrets.get_faucet_address(chain, ctx.guild.id) + "`. cc:<@712863455467667526>"

    # if the user or address has already received > max Matic, deny
    # elif faucet.get_address_balance(chain, "testnet", address) >= MAX_TOKENS_REQUESTED:
    #    response = "You have over " + str(MAX_TOKENS_REQUESTED) + token + " in your wallet. Please request more when you run out."

    # if the user has requested in the past 24 hours, deny
#    elif datetime.now() - datetime.strptime(user_db.get_user_last_transaction_time(ctx.author.id, chain), "%m/%d/%Y, %H:%M:%S") < timedelta(hours=24):
#        time_diff = datetime.now() - datetime.strptime(user_db.get_user_last_transaction_time(ctx.author.id, chain), "%m/%d/%Y, %H:%M:%S")
#        response = f"You have already requested. Please request again in: {(timedelta(days=1)-time_diff).seconds/3600} hours."

    # if the address is not valid, deny
    elif not valid_address(address):
        response = "usage: `" + prefix + "faucet [address]`. \n" \
                                         "Please enter a valid address."

    # if we passed all the above checks, proceed
    else:
        success = faucet.send_transaction(chain, "testnet", address, tokens_requested, ctx.guild.id)

        # success = True
        if success:
            user_db.add_transaction(str(ctx.author.id), datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), chain)
            response = f"Sending {str(tokens_requested)} {token} to {address[:8]}...{address[-4:]}.\nHash: {success}"

        else:
            response = "There was an issue sending funds. cc:<@712863455467667526>"

    log("testnet-faucet: " + response)
    await ctx.send(response)
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
        await ctx.send("usage: `" + prefix + "testnet [address]` cc:<@712863455467667526>")
        log(error)
        raise error


@bot.command(name='balance', help='usage: ' + prefix + 'balance')
# @commands.has_any_role(*ADMIN_DISCORD_ROLES)
async def get_testnet_balance(ctx):
    try:
        balance = faucet.get_faucet_balance("comdex", "testnet", ctx.guild.id)
        response = "The faucet has " + str(balance) + " CMDX"
        await ctx.send(response)
    except Exception as e:
        log(e)


# @bot.command(name='devnet', help='usage: ' + prefix + 'devnet [address]')
# async def devnet_faucet(ctx, address: str, tokens=0.1):
#     if "comdex" in address:
#         chain = "comdex"
#         token = "CMDX"
#         MAX_DEVNET_TOKENS_REQUESTED = secrets.MAX_COMDEX_DEVNET_TOKENS_REQUESTED
#         if tokens == 0.1:
#             tokens = secrets.MAX_COMDEX_DEVNET_TOKENS_REQUESTED
#     elif "osmo" in address:
#         chain = "osmo"
#         token = "OSMO"
#         MAX_DEVNET_TOKENS_REQUESTED = secrets.MAX_OSMOSIS_DEVNET_TOKENS_REQUESTED
#         if tokens == 0.1:
#             tokens = secrets.MAX_OSMOSIS_DEVNET_TOKENS_REQUESTED
#     else:
#         response = "usage: `" + prefix + "devnet [address]`. \n" \
#                                          "This bot only accepts Comdex and Osmosis addresses, please enter a valid address."
#         log("testnet-faucet: " + response)
#         await ctx.send(response)
#         return
#
#     if faucet.get_faucet_balance(chain, "devnet", ctx.guild.id) < tokens:
#         if faucet.get_faucet_balance(chain, "devnet", ctx.guild.id) == 0.0:
#             response = "The RPC is down, please try again later"
#         else:
#             response = "The faucet does not have enough funds."
#
#     # if the user or address has already received > max Matic, deny
#     elif faucet.get_address_balance(chain, "devnet", address) >= MAX_DEVNET_TOKENS_REQUESTED * 5:
#         response = "Please request more when you run out of tokens."
#
#     # if we passed all the above checks, proceed
#     elif valid_address(address):
#         success = faucet.send_transaction(chain, "devnet", address, tokens, ctx.guild.id)
#
#         # success = True
#         if success:
#             response = "Sent " + str(tokens) + " " + token + " to " + address[:8] + "..." + \
#                        address[-4:] + ".\nHash: " + success
#
#         else:
#             response = "There was an issue sending funds. cc:<@712863455467667526>"
#
#     else:
#         response = "usage: `" + prefix + "devnet [address]`. \n" \
#                                          "This bot only accepts Comdex addresses, please enter a valid address."
#     log("testnet-faucet: " + response)
#     await ctx.send(response)
#     return


# @devnet_faucet.error
# async def devnet_faucet_error(ctx, error):
#     if isinstance(error, BadArgument):
#         await ctx.send("usage: `" + prefix + "devnet [address]`. \n"
#                                              "Invalid address.")
#         raise error
#     elif isinstance(error, MissingRequiredArgument):
#         await ctx.send("usage: `" + prefix + "devnet [address]`")
#         raise error
#     else:
#         await ctx.send("usage: `" + prefix + "devnet [address]` cc:<@712863455467667526>")
#         log(error)
#         raise error


@bot.command(name='devnet-balance', help='usage: ' + prefix + 'devnet-balance')
# @commands.has_any_role(*ADMIN_DISCORD_ROLES)
async def get_devnet_balance(ctx):
    try:
        balance = faucet.get_faucet_balance("comdex", "devnet", ctx.guild.id)
        response = "The faucet has " + str(balance) + " CMDX"
        await ctx.send(response)
    except Exception as e:
        log(e)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


bot.run(disc_token)
