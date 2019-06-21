from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import config,os
from exts import db
from flask import Flask
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials = True) # 解决跨域问题

app.config.from_object(config)
db.init_app(app)

manager = Manager(app)
migrate = Migrate(app,db) # 使用Migrate绑定app和db
manager.add_command('db',MigrateCommand) #添加迁移脚本的命令到manager中

if __name__ == '__main__':
    manager.run()
