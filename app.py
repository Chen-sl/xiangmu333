import threading

from flask import Flask, render_template, request
import paramiko
# import  config
app = Flask(__name__)
cons=''
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/<companyCode>')
def bind(companyCode):
    aaa = {}
    global cons
    if companyCode=='03311':
        aaa=ssh2('192.168.10.82', 'fengyun', passwd, cmd)
        cons = aaa.get('content')
    else:
        aaa = ssh2('192.168.10.91', username, passwd, cmd)
        cons = aaa.get('content')
    return render_template('index.html',bindCode=cons)
@app.route('/weixin/',methods=['GET','POST'])
def weixin():
    if request.method=='GET':

        return render_template('weixin.html',bindCode=cons)
    else:
         pass
@app.route('/platform/',methods=['GET','POST'])
def platform():
    if request.method=='GET':
        return render_template('platform.html',bindCode=cons)
    else:
         pass
@app.route('/activity/',methods=['GET','POST'])
def activity():
    if request.method=='GET':
        return render_template('activity.html',bindCode=cons)
    else:
         pass
@app.route('/VIP/',methods=['GET','POST'])
def VIP():
    if request.method=='GET':
        return render_template('VIP.html',bindCode=cons)
    else:
         pass
@app.route('/congratuations/',methods=['GET','POST'])
def congratuations():
    if request.method=='GET':
        return render_template('congratuations.html',bindCode=cons)
    else:
         pass
@app.route('/split/',methods=['GET','POST'])
def split():
    if request.method=='GET':
        return render_template('split.html',bindCode=cons)
    else:
         pass
@app.route('/title/',methods=['GET','POST'])
def title():
    if request.method=='GET':
        return render_template('title.html',bindCode=cons)
    else:
         pass
@app.route('/game/',methods=['GET','POST'])
def game():
    if request.method=='GET':
        return render_template('game.html',bindCode=cons)
    else:
         pass
@app.route('/zhicheng/',methods=['GET','POST'])
def zhicheng():
    if request.method=='GET':
        return render_template('zhicheng.html',bindCode=cons)
    else:
         pass
@app.route('/KTV/',methods=['GET','POST'])
def KTV():
    if request.method=='GET':
        return render_template('KTV.html',bindCode=cons)
    else:
         pass
@app.route('/other/',methods=['GET','POST'])
def other():
    if request.method=='GET':
        return render_template('other.html',bindCode=cons)
    else:
         pass

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

            if out.find('roombindingcode') >= 0:
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
    cmd = ['cat /evideoktv/bin/gateway/data/config.ini|grep centeraddress',
           "cat /evideoktv/log/gateway.log | grep B401|tail -n 1| awk '{print $5}'",  # 获取当前绑定码
           'cat /evideoktv/bin/gateway/data/config.ini|grep centeraddress',
           "cat /evideoktv/log/history/*.log | grep B401|tail -n 1| awk '{print $5}'"  # 获取之前最新的绑定码
           ]
    username = "fengyun"  # 用户名
    passwd = "123456"  # 密码
    threads = []
    # iplist = ['192.168.10.82', '192.168.10.86', '192.168.10.91', '192.168.96.81']
    iplist = ['192.168.10.82', '192.168.10.91']

    app.run(host='0.0.0.0',debug=True,port=5000)

