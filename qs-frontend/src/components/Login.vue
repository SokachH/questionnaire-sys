<template>
  <div class="login">
    <div id="bdg">
      <canvas id="myCanvas" :width="width" :height="height"> </canvas>
    </div>
    <div class="main_login">
      <div class="title">登录</div>
      <el-row type="flex" justify="center">
        <el-form ref="loginForm" :rules="rules" :model="loginForm">
          <el-form-item prop="username">
            <el-input
              @keyup.enter.native="login('loginForm')"
              icon="el-icon-search"
              placeholder="请输入用户名"
              v-model="loginForm.username"
              class="input_style"
            >
              <i class="el-icon-user" slot="prefix"> </i>
            </el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              @keyup.enter.native="login('loginForm')"
              placeholder="请输入密码"
              class="input_style"
              v-model="loginForm.password"
              show-password
            >
              <i class="el-icon-key" slot="prefix"> </i>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-row :span="24">
              <el-col :span="13">
                <el-input
                  v-model="loginForm.code"
                  auto-complete="off"
                  placeholder="请输入验证码"
                  size=""
                  @keyup.enter.native="login('loginForm')"
                >
                  <i class="el-icon-lock" slot="prefix"> </i>
                </el-input>
              </el-col>
              <el-col :span="11">
                <div class="login_code" @click="refreshCode">
                  <s-identify :identifyCode="identifyCode"></s-identify>
                </div>
              </el-col>
            </el-row>
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              @click="login('loginForm')"
              class="submitBtn"
              >登 录</el-button
            >
          </el-form-item>
        </el-form>
      </el-row>
      <!-- 注册和忘记密码链接 -->
      <div class="link">
        <el-link type="primary" :underline="false" href="/register"
          >注册新账号</el-link
        >
        <!--<el-link type="primary" :underline="false" href="/resetpass">忘记密码</el-link>-->
      </div>
    </div>
  </div>
</template>
<script>
import { designOpera } from "./api";
import { Loading } from "element-ui";
import SIdentify from "@/components/SIdentify";
export default {
  name: "Login",
  components: {
    SIdentify,
  },
  data() {
    return {
      canvas: null,
      context: null,
      stars: [], // 星星数组
      shadowColorList: [
        "#39f",
        "#ec5707",
        "#b031d4",
        "#22e6c7",
        "#92d819",
        "#14d7f1",
        "#e23c66",
      ], //阴影颜色列表
      directionList: ["leftTop", "leftBottom", "rightTop", "rightBottom"], //星星运行方向
      speed: 50, //星星运行速度
      last_star_created_time: new Date(), //上次重绘星星时间
      Ball: class Ball {
        constructor(radius) {
          this.x = 0;
          this.y = 0;
          this.radius = radius;
          this.color = "";
          this.shadowColor = "";
          this.direction = "";
        }
        draw(context) {
          context.save();
          context.translate(this.x, this.y);
          context.lineWidth = this.lineWidth;
          var my_gradient = context.createLinearGradient(0, 0, 0, 8);
          my_gradient.addColorStop(0, this.color);
          my_gradient.addColorStop(1, this.shadowColor);
          context.fillStyle = my_gradient;
          context.beginPath();
          context.arc(0, 0, this.radius, 0, Math.PI * 2, true);
          context.closePath();

          context.shadowColor = this.shadowColor;
          context.shadowOffsetX = 0;
          context.shadowOffsetY = 0;
          context.shadowBlur = 10;

          context.fill();
          context.restore();
        }
      }, //工厂模式定义Ball类
      width: window.innerWidth,
      height: window.innerHeight,
      // 表单数据
      loginForm: {
        username: "", //用户名
        password: "", //密码
        code: "", // 验证码
      },
      identifyCodes: "1234567890abcdefjhijklinopqrsduvwxyz",
      identifyCode: "",
      rules: {
        //表单验证（用户名验证规则）
        username: [
          { required: true, message: "账号不能为空", trigger: "blur" },
          { max: 20, message: "账号长度最长20位", trigger: "blur" },
        ],
        //表单验证（密码验证规则）
        password: [
          { required: true, message: "密码不能为空", trigger: "blur" },
          { min: 6, message: "密码长度最少为6位", trigger: "blur" },
        ],
        code: [{ required: true, message: "验证码不能为空", trigger: "blur" }],
      },
    };
  },
  methods: {
    //重复动画
    drawFrame() {
      let animation = requestAnimationFrame(this.drawFrame);
      this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
      this.createStar(false);
      this.stars.forEach(this.moveStar);
    },
    //展示所有的星星
    createStar(params) {
      let now = new Date();
      if (params) {
        //初始化星星
        for (var i = 0; i < 50; i++) {
          const radius = Math.random() * 3 + 2;
          let star = new this.Ball(radius);
          star.x = Math.random() * this.canvas.width + 1;
          star.y = Math.random() * this.canvas.height + 1;
          star.color = "#ffffff";
          star.shadowColor = this.shadowColorList[
            Math.floor(Math.random() * this.shadowColorList.length)
          ];
          star.direction = this.directionList[
            Math.floor(Math.random() * this.directionList.length)
          ];
          this.stars.push(star);
        }
      } else if (!params && now - this.last_star_created_time > 3000) {
        //每隔3秒重绘修改颜色其中30个球阴影颜色
        for (var i = 0; i < 30; i++) {
          this.stars[i].shadowColor = this.shadowColorList[
            Math.floor(Math.random() * this.shadowColorList.length)
          ];
        }
        this.last_star_created_time = now;
      }
    },
    //移动
    moveStar(star, index) {
      if (star.y - this.canvas.height > 0) {
        //触底
        if (Math.floor(Math.random() * 2) === 1) {
          star.direction = "leftTop";
        } else {
          star.direction = "rightTop";
        }
      } else if (star.y < 2) {
        //触顶
        if (Math.floor(Math.random() * 2) === 1) {
          star.direction = "rightBottom";
        } else {
          star.direction = "leftBottom";
        }
      } else if (star.x < 2) {
        //左边
        if (Math.floor(Math.random() * 2) === 1) {
          star.direction = "rightTop";
        } else {
          star.direction = "rightBottom";
        }
      } else if (star.x - this.canvas.width > 0) {
        //右边
        if (Math.floor(Math.random() * 2) === 1) {
          star.direction = "leftBottom";
        } else {
          star.direction = "leftTop";
        }
      }
      if (star.direction === "leftTop") {
        star.y -= star.radius / this.speed;
        star.x -= star.radius / this.speed;
      } else if (star.direction === "rightBottom") {
        star.y += star.radius / this.speed;
        star.x += star.radius / this.speed;
      } else if (star.direction === "leftBottom") {
        star.y += star.radius / this.speed;
        star.x -= star.radius / this.speed;
      } else if (star.direction === "rightTop") {
        star.y -= star.radius / this.speed;
        star.x += star.radius / this.speed;
      }
      star.draw(this.context);
    },
    //检查登录是否过期
    logincheck() {
      designOpera({
        opera_type: "logincheck",
      }).then((data) => {
        console.log(data);
        if (data.code == 404) {
          this.$router.push({ path: "/login" });
        }
        if (data.data != null) {
          console.log(data);
          sessionStorage.setItem("username", data.data.user); //将后端传的username存入session
          this.$router.push({ path: "/home" });
        }
      });
    },
    //登录方法
    login(formName) {
      // 表单验证通过，可进行操作
      if (
        this.loginForm.code.toLowerCase() !== this.identifyCode.toLowerCase()
      ) {
        this.$message.error("请填写正确的验证码");
        this.refreshCode();
        return;
      }
      this.$refs[formName].validate((valid) => {
        if (valid) {
          designOpera({
            opera_type: "login", //操作类型
            username: this.loginForm.username, //用户名
            password: this.$md5(this.loginForm.password), //密码md5加密
          }).then((data) => {
            console.log(data);
            if (data.code == 0) {
              //登录成功，并提示
              this.$notify({
                type: "success",
                message: "欢迎你," + this.loginForm.username + "!",
                duration: 3000,
              });
              this.$router.push({ path: "/home" }); //跳转到用户主页面
              sessionStorage.setItem("username", this.loginForm.username); //将用户名存入session中
              this.$emit("state"); //将状态传到base页面
            } else {
              if (data.code == -5) {
                //未注册,友好提示未注册
                this.$message({
                  type: "error",
                  message: "您还未注册账户，请注册",
                  showClose: true,
                });
              } else {
                //账号或密码错误提示
                this.$message({
                  type: "error",
                  message: "账号或密码错误",
                  showClose: true,
                });
              }
            }
          });
        } else {
          return false; //表单验证错误返回false
        }
      });
    },
    randomNum(min, max) {
      return Math.floor(Math.random() * (max - min) + min);
    },
    refreshCode() {
      this.identifyCode = "";
      this.makeCode(this.identifyCodes, 4);
    },
    makeCode(o, l) {
      for (let i = 0; i < l; i++) {
        this.identifyCode += this.identifyCodes[
          this.randomNum(0, this.identifyCodes.length)
        ];
      }
    },
  },
  mounted() {
    this.canvas = document.getElementById("myCanvas");
    this.context = this.canvas.getContext("2d");
    this.createStar(true);
    this.drawFrame();
    this.logincheck();
    this.identifyCode = "";
    this.makeCode(this.identifyCodes, 4);
  },
};
</script>


<style>
.login {
  position: absolute;
  width: 100%;
  height: 100%;
  /* background-color: #e4e7ed; */
  background-image: url("../../static/images/1.jpg");
}
.title {
  font-size: large;
  font-weight: bolder;
  text-align: center;
  color: #ffffff;
  margin-bottom: 10px;
}
.main_login {
  position: absolute;
  left: 48%;
  top: 40%;
  width: 320px;
  height: 330px;
  margin: -190px 0 0 -190px;
  padding: 40px;
  border-radius: 5px;
  background: #f2f6fc;
  box-shadow: -15px 15px 15px rgba(6, 17, 47, 0.7);
  opacity: 1;
  background: linear-gradient(
    230deg,
    rgba(53, 57, 74, 0) 0%,
    rgb(0, 0, 0) 100%
  );
}
.el-form {
  padding-top: 5%;
  padding-left: 10%;
  padding-right: 10%;
  width: 280px;
}
.el-row {
  height: 100%;
  width: 100%;
}
.link {
  margin-top: -13%;
  text-align: center;
  margin-left: -5%;
}
.el-link {
  margin-left: 8px;
  line-height: 20px;
  font-size: 8px;
}
#bdg {
  height: 100%;
  width: 100%;
  overflow: hidden;
}
.el-input__inner {
  background-color: transparent;
  color: cornsilk;
}
.submitBtn {
  text-align: center;
  width: 150px;
  margin-top: 10px;
}
.login_code {
  height: 20px;
}
</style>
