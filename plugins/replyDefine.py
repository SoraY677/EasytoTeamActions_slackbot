from slackbot.bot import respond_to,listen_to
import re
import json
import codecs
import random

# コマンド要求
# 用意したコマンドにあったものがない場合にはコマンドの一覧を出す
@respond_to('ce(.*)', re.IGNORECASE)
def commandResult(message,commandName):
    # 空白は消し飛ばす
    commandNameTmp = str(commandName).replace(' ', '')
    #jsonファイルを開く
    jsonBuf = codecs.open("link.json",'r','utf-8')
    jsonData = json.load(jsonBuf)
    # ヘルプ用の文字列を生成
    helpstr =\
    "`ce`コマンドは空白を一つをつけた後に続けて以下をつけることでコマンドを実行可能です\n" + \
    "(ex) `ce hogehoge`\n\n"
    for jsonName in jsonData:
        helpstr += " - `" + jsonName + "` :" + jsonData[jsonName]["author_name"] + "\n"
        if commandNameTmp == jsonName:
            message.send_webapi('', json.dumps([jsonData[commandNameTmp]],ensure_ascii=False))
            jsonBuf.close()
            return True
    
    message.reply(helpstr)
    jsonBuf.close();
    return False

# アンケート機能(Max10個)
# `ancate <タイトル名> <選択肢1> <選択肢2> ... <選択肢9>`
@listen_to("ancate (.*)")
def ancateCommand(message, ancateStr):
    EMOJIS = ["one","two","three","four","five","six","seven","eight","nine"]
    strArray = str(ancateStr).split(' ')
    resultStr = str(message.user["id"]) + "さんよりアンケートです！\n"
    resultStr += "**"+ strArray[0]+"**\n"

    for select_i in range(1,len(strArray)):
        resultStr += " :"+EMOJIS[select_i-1]+": " + strArray[select_i] + "\n"

    post = {
        'text': resultStr
    }

    ret = message._client.webapi.chat.post_message(
        message._body['channel'],
        '',
        username=message._client.login_data['self']['name'],
        as_user=True,
        attachments=[post]
    )
    ts = ret.body['ts']
    for select_i in range(1,len(strArray)):
        message._client.webapi.reactions.add(
            name=EMOJIS[select_i-1],
            channel=message._body['channel'],
            timestamp=ts
        )


# ルーレットで指定の人の順番を決めるやつ
@listen_to("rc (.*)")
def rouletteChooser(message,chooserList):
    #選択された人たちを配列にする
    chooserArray = str(chooserList).split(" ")
    message.send("ランダムルーレットの結果は以下の通りです")
    result = random.sample(chooserArray,len(chooserArray))
    for i in range(len(result)):
        message.send(str(i+1) + "番目の人：" + result[i])
    
@listen_to("rctest")
def rctest(message):
    tmp = message.user;
    print(tmp);
    message.send(json.dumps(tmp));
