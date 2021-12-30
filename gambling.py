import discord
import random
def winnerMsg (): 
    global winner, settings 
    id = int(settings['sessionID'])
    settings['sessionID'] = id +1 
    return "Congratulations "+winner.name +' for winning BINGO session ' + str(id) +"!"
def verify(board):
    global bingoSession, bingo, bingoEnded, rolls
    length = 5
    check = False 
    for i in range (0,length): 
        check = True 
        rowCheck = i 
        while rowCheck < rowCheck+length: 
            if not board[rowCheck] in rolls:
                check = False 
                break
            rowCheck+=1
        if check: 
            break
        colCheck = i
        while colCheck <len(board): 
            if not board[colCheck] in rolls: 
                check = False
                break 
            colCheck+=length
    if check: 
        bingoEnded = True 
    else: 
        leftDiagonal = 0 
        while leftDiagonal<len(board): 
            if not board[leftDiagonal] in rolls:
                check = False
                break
            leftDiagonal+=length+1
        if check: 
            bingoEnded = True
        rightDiagonal = length-1
        while rightDiagonal<len(board):
            if not board[rightDiagonal] in rolls: 
                check = False 
                break
            rightDiagonal+=length-1
        if check: 
            bingoEnded = True 
        else: 
            bingo = False
async def verifyingLinks (): 
    global bingoSession, link, verifying 
    completeLine = "Verifying "+verifying.name +":\n"
    for index,author in enumerate(bingoSession):
        if author.name == verifying.name: 
            completeLine+=link+str(index+1)+"\n"
    completeLine = completeLine.strip()
    await channels[settings['config']].send(completeLine)
async def sendAllInvites (bingoSession, link): 
    invites = dict() 
    for index, author in enumerate(bingoSession):
        if author in invites: 
            invites[author].append(link+str(index+1))
        else: 
            invites[author] = [link+str(index+1)]
    for user in invites:
        lst = invites[user]
        line = "Your bingo boards: \n"
        for l in lst: 
            line+=l+"\n"
        line = line.strip() 
        await user.send(line)
async def updateGame (newMsg, canRoll): 
    global bingo, bingoEnded, channels, rolls, currentBingoMessage, sessionStarted, settings
    if sessionStarted:
        if newMsg:
            currentBingoMessage = await channels[settings['bingo']].send(writeBingoGameStatus(canRoll)); 
        else: 
            await currentBingoMessage.edit(content=writeBingoGameStatus(canRoll))
def writeBingoStatus (bingoSession, registered):
    completeLine = "Bingo session has been initiated with "+ str(len(bingoSession)) + " players in mind!\n"+str(len(registered))+"/"+str(len(bingoSession))+" players are currently locked in.\n"
    for index,b in enumerate(bingoSession): 
        completeLine+=str(index+1)+": "
        if not b is None:
            completeLine+=b.name
        completeLine+="\n"
    completeLine = completeLine.strip()
    return completeLine
def writeBingoGameStatus (canRoll):
    global bingo,bingoEnded, verifying, winner, rolls
    completeLine = ""
    status = ""
    header = "--------------Bingo Game Status--------------\nRemember to type BINGO in the chat once BINGO is reached!\n"
    if bingo and bingoEnded: 
        status = "Bingo Status: Ended and verified! Board won! Congraulations "+ winner.name
    elif bingo: 
        status = "Bingo status: Verifying BINGO claim from "+ verifying.name
    elif canRoll: 
        if len(rolls)<101:
            roll = random.randint(1,101)
            while roll in rolls: 
                roll = random.randint(1,101)
            rolls.append(roll)
            status = "Bingo status: Rolled a "+ str(rolls[-1]) +".\n"
        else:
            status = "Bingo status: Ran out of rolls so better call BINGO now.\n"
    rollsOutput = "Current rolls: "+ str(rolls)
    completeLine = header+"\n"+status+"\n"+rollsOutput
    return completeLine
global bingoSession, bingo, originalMessageSetup, numBingoSession, link, verifying, winner, currentBingoMessage
token = 'OTExNDk2ODMyMTE3NTM0NzIw.YZiPkw.Y3bcTFocyH4nS1UljLJYtdbQ_Ug'
client = discord.Client()
channels = dict()
characterInitialized = "!"
bingoSession = [] 
rolls = [] 
bingo = False
currentBingoMessage = None 
bingoEnded = False 
verifying = None 
winner = None
numbers = [] 
originalMessageSetup = None
numBingoSession = -1
sessionStarted = False
registered = [] 
link = ""
help = ""
adminHelp = ""
settings = dict()

@client.event
async def on_ready():
    global token, client, channels, characterInitialized, bingoSession
    global bingo, originalMessageSetup, numBingoSession, link, settings, help, adminHelp
    sampleChannels = []
    for channel in client.get_all_channels():
        sampleChannels.append(channel)
    '''
    completeLine = ""
    for c in sampleChannels:
        completeLine+=str(c.name)+"\n"
    completeLine = completeLine.strip() 
    print(completeLine)
    with open('./channels.txt', 'w') as f:
        f.write(completeLine)
    '''
   
    with open('./channels.txt', 'r', encoding='utf8') as f:
        channelNames = f.readlines() 
        for index,l in enumerate(channelNames): 
            channelNames[index] = l.strip() 
    with open('./settings.txt', 'r', encoding='utf8') as f:
        settingLines = f.readlines()
        for setting in settingLines: 
            splitSetting = setting.split(' ')
            settings[splitSetting[0]] = splitSetting[1].strip()
    with open('./help.txt', 'r', encoding='utf8') as f:
        lines = f.readlines()
        for h in lines: 
            help+=h
    with open('./adminHelp.txt', 'r', encoding='utf8') as f:
        lines = f.readlines()
        for h in lines: 
            adminHelp+=h
    for s in sampleChannels: 
        if s.name in channelNames: 
            channels[s.name] = s
    numBingoSession = settings['sessionID']
    
@client.event
async def on_message(message):
    global token, client, channels, characterInitialized, bingoEnded, settings, rolls, help, adminHelp
    global bingoSession, bingo, originalMessageSetup, numBingoSession, link, sessionStarted, verifying, winner, registered

    print(message.content)
    print(message.author)
    prefix = message.content[0]
    rest_message = message.content[1:]
    if prefix == characterInitialized:
        arguments = rest_message.split(" ")
        initial_argument = arguments[0]
        preceding_argument = arguments[1]
        if initial_argument=='bingo':
            print(settings)
            if preceding_argument=='init' and message.channel.name == settings['config']:
                rest_arguments = arguments[2:]
                registered = [] 
                bingoEnded = False
                numBingoSession = int(rest_arguments[0]) 
                bingoSession = [None for i in range(numBingoSession)]
                completeLine = writeBingoStatus(bingoSession, registered)
                originalMessageSetup = await channels[settings['bingo']].send(completeLine)
            elif preceding_argument=='save' and message.channel.name == settings['config']:
                completeLine = ""
                for s in settings: 
                    line = s +" "+str(settings[s]) 
                    completeLine+=line+"\n"
                completeLine = completeLine.strip() 
                with open('./settings.txt', 'w', encoding='utf8') as f: 
                    f.write(completeLine)
                await channels[settings['config']].send("Settings are saved with these settings listed below: \n"+completeLine)
            else:
                if bingoEnded:
                    if preceding_argument == 'help':
                        if message.channel.name == settings['config']: 
                            completeLine = adminHelp+"\n\nRemember to post your commands in the "+settings['config']+" channel in order for the commands to work!"
                            await channels[settings['config']].send(completeLine)
                        else:
                            completeLine = help+"\n\nRemember to post your commands in the "+settings['bingo']+" channel in order for the commands to work!"
                            await message.channel.send(completeLine)
                    elif preceding_argument == 'revert' and message.channel.name == settings['config']:
                        if sessionStarted:
                            bingoEnded = False 
                            bingo = False 
                            await updateGame(True, True)
                    else:
                        await channels[settings['bingo']].send("There is no session currently set up!")
                else:
                    if preceding_argument == 'register':
                        rest_arguments = arguments[2:]
                        failed = [] 
                        successful = [] 
                        rest_arguments = arguments[2:]
                        if rest_arguments[0] == 'all': 
                            for i in range (1,numBingoSession+1): 
                                if not i in registered and not bingoSession[i-1] is None:
                                    registered.append(i)
                                elif bingoSession[i] is None:
                                    failed.append(i)
                        else:
                            for num in rest_arguments:
                                num = int(num)
                                if num<=len(bingoSession) and bingoSession[num-1] is None: 
                                    bingoSession[num-1] = message.author
                                    successful.append(num)
                                    registered.append(num)
                                else:
                                    failed.append(num)
                        otherLine = ""
                        if (len(successful)>0):
                            otherLine+='Successfully registered '
                            for s in successful: 
                                otherLine+=str(s)+","
                            otherLine = otherLine[:-1]
                            otherLine += " slots.\n"
                        if (len(failed)>0): 
                            otherLine+= 'Failed to register '
                            for f in failed: 
                                otherLine+=str(f)+","
                            otherLine = otherLine[:-1]
                            otherLine += ' slots.'
                        otherLine = otherLine.strip()
                        await message.reply(otherLine)
                        sessionStarted = len(registered)>=len(bingoSession) and len(link)>0
                        completeLine = writeBingoStatus(bingoSession, registered)
                        if sessionStarted: 
                            await channels[settings['bingo']].send('Bingo registration has closed! Bingo session will commence shortly!')
                            await sendAllInvites(bingoSession, link)
                        else: 
                            currentFillStatus = str(len(registered)) +"/"+str(len(bingoSession)) +" players are registered\n"
                            linkStatus = "Link has not been initialized yet either!"
                            await channels[settings['config']].send(currentFillStatus +linkStatus)
                        if message.channel.name == settings['bingo']:
                            originalMessageSetup = await channels[settings['bingo']].send(completeLine)
                        else: 
                            await originalMessageSetup.edit(content=completeLine)
                    elif preceding_argument == 'link':
                        link = arguments[2]
                        await channels[settings['config']].send('Links have been embedded successfully!')
                        sessionStarted = len(registered)>=numBingoSession and len(link)>0
                        if sessionStarted:
                            await channels[settings['bingo']].send('Bingo registration has closed! Bingo session will commence shortly!')
                            await sendAllInvites(bingoSession, link)
                    elif preceding_argument == 'help':
                        if message.channel.name == settings['config']: 
                            completeLine = adminHelp+"\n\nRemember to post your commands in the "+settings['config']+" channel in order for the commands to work!"
                            await channels[settings['config']].send(completeLine)
                        else:
                            completeLine = help+"\n\nRemember to post your commands in the "+settings['bingo']+" channel in order for the commands to work!"
                            await message.channel.send(completeLine)
                            if message.channel.name == settings['bingo']: 
                                if not originalMessageSetup is None:
                                    completeLine = writeBingoStatus(bingoSession, registered)
                                    originalMessageSetup = await channels[settings['bingo']].send(completeLine) 
                    elif preceding_argument == 'kick' and message.channel.name == settings['config']:
                        rest_arguments = arguments[2:]
                        successfulKick = [] 
                        failedKick = []
                        errMsg = ""
                        for num in rest_arguments: 
                            num = int(num)
                            if num>0 and num<len(bingoSession) and num in registered:
                                registered.remove(num)
                                bingoSession[num-1] = None 
                                successfulKick.append(num)
                            else:
                                failedKick.append(num)
                        errMsg = errMsg.strip() 
                        if len(successfulKick)>0:
                            await channels[settings['config']].send(str(successfulKick) +" successfully kicked.")
                        if len(failedKick)>0:
                            await channels[settings['config']].send(str(successfulKick) +" successfully kicked.")
                        sessionStarted = False 
                        await originalMessageSetup.edit(content=writeBingoStatus(bingoSession, registered))
                    elif preceding_argument == 'start' and message.channel.name == settings['config']: 
                        if sessionStarted and len(rolls)==0: 
                            await channels[settings['config']].send("Bingo session has officially started!")
                            await updateGame(True, True)
                        else: 
                            await channels[settings['config']].send("Bingo session is not ready yet!")
                            if originalMessageSetup is None:
                                originalMessageSetup = await channels[settings['bingo']].send(writeBingoStatus(bingoSession, registered))
                            else:
                                await originalMessageSetup.edit(content=writeBingoStatus(bingoSession, registered))
                    elif preceding_argument == 'roll' and message.channel.name == settings['config']: 
                        if sessionStarted and verifying is None: 
                            await updateGame(False, True)
                        else: 
                            await updateGame(True, True)
                    elif preceding_argument == 'win' and message.channel.name == settings['config']:
                        bingoEnded = True 
                        winner = verifying
                        await updateGame(True,False)
                        await channels[settings['winner']].send(winnerMsg())
                    elif preceding_argument == 'kap':
                        bingo = False
                        verifying = None 
                        await channels[settings['bingo']].send('KAP... Continuing on the game.')
                        await updateGame(True,False)
                    elif preceding_argument == 'reset' and message.channel.name == settings['config']:
                        bingoSession = [] 
                        registered = [] 
                        bingoEnded = False
                        bingo = False 
                        originalMessageSetup = None
                        numBingoSession = settings['sessionID']
                        link = ""
                        verifying=None
    else: 
        if bingoSession:
            if message.content == 'BINGO' and message.channel.name == settings['bingo']: 
                if not bingo:
                    guy = message.author
                    bingo = guy in bingoSession
                    if bingo:
                        verifying = guy
                        await verifyingLinks()
                        await updateGame(True, False)
                    else: 
                        await channels[settings['bingo']].send('Sorry, I don\'t think you are in our current session!')
                        await updateGame(True, False)
                else: 
                    await channels[settings['bingo']].send('Currently verifying another player at the moment!')
                    await updateGame(True, False)
client.run(token)