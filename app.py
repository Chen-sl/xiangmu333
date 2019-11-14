import threading

from flask import Flask, render_template, request
import paramiko

app = Flask(__name__)
bindCode=''
ww_url='http://www.ktvme.com'
@app.route('/')
def index():

    return render_template('index.html')
@app.route('/bind/',methods=['GET','POST'])
def bind():
    codeDic = {}
    global bindCode
#    global ww_url
#   ww_url = "http://www.ktvme.com"


    print('1111111111111111')
    print(request.form.get('codeEnter'))
    if request.form.get('codeEnter')=='':
        stbip = request.form.get('stbip')
        if stbip.find('96123')>0:
            try:
                codeDic = ssh2_km2('192.168.96.121', 'fengyun', '123456', stbip)
                print(codeDic)
                bindCode = codeDic.get('content')  #cons等于绑定码
            except Exception:
                print("没有获取到绑定码！！！")
        else:
            try:
                codeDic = ssh2_km2('192.168.96.72', 'fengyun', '123456',stbip)
                bindCode = codeDic.get('content')
            except Exception:
                print("没有获取到绑定码！！！")
    else:
        bindCode=request.form.get('codeEnter')
        print('这是输入的绑定码%s' % bindCode)
    return render_template('index.html',bindCode=bindCode)


@app.route('/weixin/',methods=['GET','POST'])
def weixin():
    if request.method=='GET':
        print('xxxxxxxxxxxxxxxxxxxx')
        print(bindCode)
        return render_template('weixin.html',bindCode=bindCode)
    else:
         pass
@app.route('/platform/',methods=['GET','POST'])
def platform():
    if request.method=='GET':
        return render_template('platform.html',bindCode=bindCode)
       # return render_template('platform.html', ww_url=ww_url)
    else:
         pass
@app.route('/activity/',methods=['GET','POST'])
def activity():
    if request.method=='GET':
        return render_template('activity.html',bindCode=bindCode)
    else:
         pass
@app.route('/VIP/',methods=['GET','POST'])
def VIP():
    if request.method=='GET':
        return render_template('VIP.html',bindCode=bindCode)
    else:
         pass
@app.route('/congratuations/',methods=['GET','POST'])
def congratuations():
    if request.method=='GET':
        return render_template('congratuations.html',bindCode=bindCode)
    else:
         pass
@app.route('/split/',methods=['GET','POST'])
def split():
    if request.method=='GET':
        return render_template('split.html',bindCode=bindCode)
    else:
         pass
@app.route('/title/',methods=['GET','POST'])
def title():
    if request.method=='GET':
        return render_template('title.html',bindCode=bindCode)
    else:
         pass
@app.route('/game/',methods=['GET','POST'])
def game():
    if request.method=='GET':
        return render_template('game.html',bindCode=bindCode)
    else:
         pass
@app.route('/zhicheng/',methods=['GET','POST'])
def zhicheng():
    if request.method=='GET':
        return render_template('zhicheng.html',bindCode=bindCode)
    else:
         pass
@app.route('/KTV/',methods=['GET','POST'])
def KTV():
    if request.method=='GET':
        return render_template('KTV.html',bindCode=bindCode)
    else:
         pass
@app.route('/other/',methods=['GET','POST'])
def other():
    if request.method=='GET':
        return render_template('other.html',bindCode=bindCode)
    else:
        pass


def ssh2_km2(ip, username, passwd,stbip):
        cmd=[]
        ping=''
        if stbip.find('96123')>0:
            ping = "ping.sh 192.168.96.123"
        elif stbip.find('96075')>0:
            ping = "ping.sh 192.168.96.75"
        elif stbip.find('96076')>0:
            ping = "ping.sh 192.168.96.76"
        elif stbip.find('10104')>0:
            ping = "ping.sh 192.168.10.104"
        elif stbip.find('96077')>0:
            ping = "ping.sh 192.168.96.77"
        elif stbip.find('96078')>0:
            ping = "ping.sh 192.168.96.78"
        head1 = "cat /evideoktv/log/gateway.log | grep B401| grep " #获取新的网关B401日志
        head2 = "cat /evideoktv/log/history/*.log | grep B401| grep "# 获取旧的网关B401日志
        tail ="| awk '{print $5}'| tail -1"    #截取roombindingcode 最新的一条
        newlog = head1+stbip+tail  #变量拼接完整获取新的绑定码 （为什么要设置成这种变量的形式，因为stbip是更具端传过来变化的）
        oldlog = head2+stbip+tail  #变量拼接完整获取旧的绑定码
        cmd.append(ping)  # 执行ping的命令
        cmd.append(newlog) #执行获取新的绑定码的命令
        cmd.append(oldlog) #执行获取旧的绑定码的命令
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, 22, username, passwd, timeout=5)


            '''从远程服务器上获取包厢绑定码'''
            #notice = ''
            content = 'default'
            for m in cmd:

                # print "cmd="+ m
                stdin, stdout, stderr = ssh.exec_command(m)
                out = stdout.readline()

                # print 'out = '+ out

                if out.find('服务器不在线') >= 0:
                    content = '当前包厢机顶盒不在线,请手动输入'
                    break

                if out.find(stbip) >= 0:
                    # content = '体验包厢[T66横]绑定码 = '
                    bindcode = out.split('=')[1].strip('\n') #分离除roombindingcode=后面的字段
                    print(bindcode)
                    content = bindcode.replace('"', '')  #去掉霜引号
                    # content += notice
                    # content += '\n'
                    break
            ssh.close()
            contents = {}
            print('2222222222222222222222222222222222222')
            print(content)
            contents['content'] = content
            return contents
        except Exception as e:
            print('ERROR', e)

def ssh2(ip, username, passwd, cmd):
    global content

    #
    # for ip in iplist:
    #     threads.append(threading.Thread(target=ssh2, args=(ip, username, passwd, cmd)))  # 添加到线程池中
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, username, passwd, timeout=5)

        '''从远程服务器上获取包厢绑定码'''
        for m in cmd:
            stdin, stdout, stderr = ssh.exec_command(m)
            out = stdout.readline()
            content = ''
            print("11111111111111111"+out)
            if out.find('company.ktvme.com') >= 0:
                # content = '外网环境包厢绑定码 = '
                continue

            if out.find('192.168.96.24') >= 0:
                # content = '内网环境包厢绑定码 = '
                continue

            if out.find('roombindingcode') and out.find('') >= 0:
                bindcode = out.split('=')[1]
                content += bindcode.replace('"', '')
                print (content)
                break  # 如果在当前日志中未获取到绑定码,则从历史记录中获取最新的一个
            else:
                content = '' #如果没有包厢绑定码则置空
        print("绑定码是："+content)
        # with open(targetfile, 'a+') as f:
        #     f.write(content)

        ssh.close()
        contents = {}
        contents['content'] = content
        return contents

    except Exception as e:
        print ('ERROR', e)


if __name__ == '__main__':
    # 获取K米体验包厢二维码
    # cmd_hq1 = [
    #     "ping.sh 192.168.96.75",
    #     "cat /evideoktv/log/gateway.log | grep B401| grep 108204096075| awk '{print $5}'| tail -1",  # 96.75 08204机顶盒
    #     "cat /evideoktv/log/history/*.log | grep B401| grep 108204096075 | awk '{print $5}'| tail -1"  # 获取之前最新的绑定码
    #
    # ]
    #
    # cmd_hq2 = [
    #     "ping.sh 192.168.96.76",
    #     "cat /evideoktv/log/gateway.log | grep B401| grep 108204096076 | awk '{print $5}'| tail -1",  # 96.76 08204机顶盒
    #     "cat /evideoktv/log/history/*.log | grep B401| grep 108204096076 | awk '{print $5}'| tail -1"]  # 获取之前最新的绑定码
    #
    # cmd_hq3 = [
    #     "ping.sh 192.168.10.104",
    #     "cat /evideoktv/log/gateway.log | grep B401| grep 108204010104 | awk '{print $5}'| tail -1",  # 10.104 08204机顶盒
    #     "cat /evideoktv/log/history/*.log | grep B401| grep 108204010104 | awk '{print $5}'| tail -1"]  # 获取之前最新的绑定码
    # cmd_hq4 = [
    #     "ping.sh 192.168.96.77",
    #     "cat /evideoktv/log/gateway.log | grep B401| grep 108204096077| awk '{print $5}'| tail -1",  # 96.77 08204机顶盒
    #     "cat /evideoktv/log/history/*.log | grep B401| grep 108204096077 | awk '{print $5}'| tail -1"]  # 获取之前最新的绑定码
    #
    # cmd_hq5= [
    #     "ping.sh 192.168.96.78",
    #     "cat /evideoktv/log/gateway.log | grep B401| grep 108204096078 | awk '{print $5}'| tail -1",  # 96.78 08204机顶盒
    #     "cat /evideoktv/log/history/*.log | grep B401| grep 108204096078 | awk '{print $5}'| tail -1"]  # 获取之前最新的绑定码
    # cmd_hq6 = [
    #     "ping.sh 192.168.96.123",
    #     "cat /evideoktv/log/gateway.log | grep B401| grep 103311096123 | awk '{print $5}'| tail -1",  # 96.123 03311机顶盒
    #     "cat /evideoktv/log/history/*.log | grep B401| grep 103311096123 | awk '{print $5}'| tail -1"]  # 获取之前最新的绑定码
    # cmd_list = [cmd_hq1, cmd_hq2, cmd_hq3,cmd_hq4,cmd_hq5,cmd_hq6]
    #
    # cmd = ['cat /evideoktv/bin/gateway/data/config.ini|grep centeraddress',
    #        "cat /evideoktv/log/gateway.log | grep B401|tail -n 1| awk '{print $5}'",  # 获取当前绑定码
    #        'cat /evideoktv/bin/gateway/data/config.ini|grep centeraddress',
    #        "cat /evideoktv/log/history/*.log | grep B401|tail -n 1| awk '{print $5}'"  # 获取之前最新的绑定码
    #        ]
    username = "fengyun"  # 用户名
    passwd = "123456"  # 密码
    threads = []
    # iplist = ['192.168.10.82', '192.168.10.86', '192.168.10.91', '192.168.96.81']
    # iplist = ['192.168.96.121', '192.168.96.72']

    app.run(host='0.0.0.0',debug=True,port=5000)

