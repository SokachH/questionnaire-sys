<template>
  <div class="register">
    <div id="bdg">
      <canvas id="myCanvas" :width="width" :height="height"> </canvas>
    </div>
    <div class="main-register">
      <div class="title">注 册</div>
      <!-- 注册表单 -->
      <el-row>
        <el-form
          :model="registerForm"
          status-icon
          :rules="rules"
          size="medium"
          ref="registerForm"
          label-width="100px"
          class="demo-registeForm"
        >
          <el-form-item prop="username" label="用户名" class="regist_form">
            <el-input
              class="regist_input"
              @keyup.enter.native="Register('registerForm')"
              v-model="registerForm.username"
              placeholder="请输入用户名"
            ></el-input>
          </el-form-item>
          <el-form-item prop="email" label="邮箱" class="regist_form">
            <el-input
              class="regist_input"
              @keyup.enter.native="Register('registerForm')"
              v-model="registerForm.email"
              placeholder="请输入邮箱"
            ></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="pass" class="regist_form">
            <el-input
              class="regist_input"
              @keyup.enter.native="Register('registerForm')"
              v-model="registerForm.pass"
              autocomplete="off"
              placeholder="请输入密码(不少于6位)"
              show-password
            >
            </el-input>
          </el-form-item>
          <el-form-item label="确认密码" prop="checkPass" class="regist_form">
            <el-input
              class="regist_input"
              @keyup.enter.native="Register('registerForm')"
              v-model="registerForm.checkPass"
              autocomplete="off"
              placeholder="请再次输入密码"
              show-password
            >
            </el-input>
          </el-form-item>
          <el-form-item label="验证码" prop="code" class="regist_form">
            <el-row :span="24">
              <el-col :span="12">
                <el-input
                  class="regist_input"
                  @keyup.enter.native="Register('registerForm')"
                  v-model="registerForm.code"
                  autocomplete="off"
                  placeholder="请输入验证码"
                >
                </el-input>
              </el-col>
              <el-col :span="12">
                <div class="login_code" @click="refreshCode">
                  <s-identify :identifyCode="identifyCode"></s-identify>
                </div>
              </el-col>
            </el-row>
          </el-form-item>
          <!-- 注册，重置按钮 -->
          <el-form-item style="margin-left: -25%; margin-top: 10px">
            <el-button type="primary" @click="Register('registerForm')"
              >注册</el-button
            >
            <el-button
              @click="resetForm('registerForm')"
              style="margin-right: -5%"
              >重置</el-button
            >
          </el-form-item>
        </el-form>
      </el-row>
      <!-- 登录页面链接 -->
      <div class="link">
        <el-link type="primary" :underline="false" href="/login"
          >已有账号?去登录</el-link
        >
      </div>
    </div>
  </div>
</template>

<script>
import { designOpera } from "./api";
import SIdentify from "@/components/SIdentify";
export default {
  name: "Register",
  components: {
    SIdentify,
  },
  data() {
    // 检查密码
    var validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      } else {
        if (this.registerForm.checkPass !== "") {
          this.$refs.registerForm.validateField("checkPass");
        }
        callback();
      }
    };
    // 确认密码验证
    var validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.registerForm.pass) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    };
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
      registerForm: {
        email: "",
        username: "", // 用户名
        pass: "", // 密码
        checkPass: "", // 检查密码
        code: "", //验证码
      },
      identifyCodes: "1234567890abcdefjhijklinopqrsduvwxyz",
      identifyCode: "",
      // 验证规则
      rules: {
        // 用户名验证规则
        username: [
          { required: true, message: "账号不能为空", trigger: "blur" },
          { max: 20, message: "账号长度最长20位", trigger: "blur" },
        ],
        email: [
          { required: true, message: "邮箱不能为空", trigger: "blur"},
        ],
        // 密码验证规则
        pass: [
          { required: true, validator: validatePass, trigger: "blur" },
          { min: 6, message: "密码长度最少为6位", trigger: "blur" },
          { max: 16, message: "密码长度不能超过16位", trigger: "blur" },
        ],
        // 检查密码验证规则
        checkPass: [
          { required: true, validator: validatePass2, trigger: "blur" },
        ],
        code: [{ required: true, message: "验证码不能为空", trigger: "blur" }],
      },
    };
  },
  // 方法定义
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
          return false;
        } else if (data.data != null) {
          console.log(data);
          sessionStorage.setItem("username", data.data.user); //将后端传的username存入session
          this.$router.push({ path: "/home" });
        }
      });
    },
    // 注册
    Register(formName) {
      if (
        this.registerForm.code.toLowerCase() !== this.identifyCode.toLowerCase()
      ) {
        this.$message.error("请填写正确的验证码");
        this.refreshCode();
        return;
      }
      // 表单验证通过，可进行操作
      this.$refs[formName].validate((valid) => {
        if (valid) {
          designOpera({
            opera_type: "register", //操作类型
            username: this.registerForm.username, //用户名
            email: this.registerForm.email,
            password: this.$md5(this.registerForm.pass), //密码md5加密
          }).then((data) => {
            console.log(data);
            if (data.code == 0) {
              //注册成功
              this.$message({
                message: "注册成功，请登录!",
                type: "success",
              });
              this.$router.push({ path: "/login" });
            } else {
              //注册失败
              this.$message({
                type: "error",
                message: "该用户名已被注册",
                showClose: true,
              });
            }
          });
        } else {
          //表单验证失败，返回false
          console.log("error submit!!");
          return false;
        }
      });
    },
    // 表单重置
    resetForm(formName) {
      this.$refs[formName].resetFields();
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
  // 页面初始化
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

<style scoped>
.register {
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: #e4e7ed;
  background-image: url("../../static/images/1.jpg");
}
.title {
  font-size: large;
  font-weight: bolder;
  text-align: center;
  color: #ffffff;
  margin-bottom: 10px;
}
.main-register {
  position: absolute;
  left: 48%;
  top: 40%;
  width: 350px;
  height: 400px;
  margin: -190px 0 0 -190px;
  padding: 40px;
  border-radius: 5px; /*圆角边框*/
  background: #f2f6fc;
  box-shadow: -15px 15px 15px rgba(6, 17, 47, 0.7);
  opacity: 1;
  background: linear-gradient(
    230deg,
    rgba(53, 57, 74, 0) 0%,
    rgb(0, 0, 0) 100%
  );
}
.regist_form >>> .el-form-item__label {
  color: #ffffff;
}
.el-form {
  padding-top: 5%;
  padding-right: 10%;
}
.el-form-item {
  margin-left: -10%;
}
.el-row {
  height: 100%;
  width: 100%;
}
.link {
  margin-top: -12%;
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
.login_code {
  height: 20px;
}
.regist_input >>> .el-input__inner {
  background-color: transparent;
  color: cornsilk;
}
</style>
