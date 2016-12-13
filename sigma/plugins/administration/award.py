from config import permitted_id
from sigma.core.permission import check_admin


async def award(cmd, message, args):
    if message.author.id in permitted_id or check_admin(message.author, message.channel):
        if message.mentions:
            target = message.mentions[0]
            if target.bot:
                await cmd.bot.send_message(message.channel, 'Can\'t award bots.')
                return
            qry = {
                'ServerID': message.server.id,
                'UserID': target.id
            }
            data = cmd.db.find('PointSystem', qry)
            curr_pts = 0
            for result in data:
                curr_pts = result['Points']
            try:
                amount = abs(int(args[0]))
                new_pts = curr_pts + amount
            except:
                await cmd.bot.send_message(message.channel, 'Not a valid point number input.')
                return
            updatetarget = {"UserID": target.id, "ServerID": message.server.id}
            updatedata = {"$set": {
                'Points': new_pts
            }}
            cmd.db.update_one('PointSystem', updatetarget, updatedata)
            await cmd.bot.send_message(message.channel, 'Okay <@' + message.author.id + '>. I have given **' + args[
                0] + '** points to <@' + target.id + '>!')
            try:
                await cmd.bot.send_message(target, 'Congrats! :gem:\nYou have been given **' + str(
                    amount) + '** points on **' + message.server.name + '** by **' + message.author.name + '**.')
            except:
                pass
        else:
            await cmd.bot.send_message(message.channel, cmd.help())
    else:
        await cmd.bot.send_message(message.channel, 'Insufficient Permissions.')
