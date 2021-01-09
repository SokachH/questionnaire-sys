<template>
  <div class="rpw">
    <div id="bdg">
      <canvas id="myCanvas" :width="width" :height="height"> </canvas>
    </div>
    <div class="main-rpw">
      <div class="title">重 置 密 码</div>
      <el-row>
        <!-- 重置密码表单 -->
        <el-form
          :model="rpwForm"
          status-icon
          :rules="rules"
          ref="rpwForm"
          label-width="100px"
          class="demo-rpwForm"
        >
          <el-form-item prop="username" label="用户名" class="reset_form">
            <el-input
              class="reset_input"
              @keyup.enter.native="rpw('rpwForm')"
              v-model="rpwForm.username"
              placeholder="请输入用户名"
            ></el-input>
          </el-form-item>
          <el-form-item prop="email" label="邮  箱" class="reset_form">
            <el-input
              class="reset_input"
              @keyup.enter.native="rpw('rpwForm')"
              v-model="rpwForm.email"
              placeholder="请输入邮箱"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <!-- 提示信息 -->
            <p style="margin: -5% 0 0 -32%; font-size: 5px; color: #ffffff;">
              重置后的密码会发送至该邮箱
            </p>
          </el-form-item>
          <el-form-item style="margin: -5% 0 0 -12%">
            <!-- 重置密码提交按钮 -->
            <el-button
              type="primary"
              @click="rpw('rpwForm')"
              style="text-align: center; width: 225px"
              >提交</el-button
            >
          </el-form-item>
        </el-form>
      </el-row>
      <div class="link">
        <!-- 跳转登录页面链接 -->
        <el-link type="primary" :underline="false" href="/login"
          >想起密码了?去登录</el-link
        >
      </div>
    </div>
  </div>
</template>

<script>
import { designOpera } from "./api";
export default {
  name: "ResetPass",
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
      rpwForm: {
        username: "", //用户名
        email: "", //邮箱
      },
      // 验证规则
      rules: {
        // 用户名验证规则
        username: [
          { required: true, message: "账号不能为空", trigger: "blur" },
          { max: 20, message: "账号长度最长20位", trigger: "blur" },
        ],
        // 邮箱验证规则
        email: [
          { required: true, message: "请输入邮箱地址", trigger: "blur" },
          {
            type: "email",
            message: "请输入正确的邮箱地址",
            trigger: ["blur", "change"],
          },
        ],
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
    // 重置密码
    rpw(formName) {
      // 表单验证通过，可进行操作
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // 确认操作
          this.$confirm("此操作将重置绑定该邮箱的账户密码, 是否继续?", "提示", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "warning",
          })
            .then(() => {
              //确定时执行操作
              designOpera({
                opera_type: "resetpass",
                username: this.rpwForm.username,
                email: this.rpwForm.email,
              }).then((data) => {
                if (data.code == 0) {
                  this.$notify({
                    title: "重置密码成功",
                    message: "新密码已发送至您的邮箱，请注意查收!(此功能正在开发中)",
                    type: "success",
                  });
                  this.$router.push({ path: "/login" });
                } else {
                  if (data.code == -5) {
                    this.$message({
                      type: "error",
                      message: "您还未注册账户，请注册",
                      showClose: true,
                    });
                  } else if (data.code == -10) {
                    this.$message({
                      type: "error",
                      message: "您还未绑定邮箱",
                      showClose: true,
                    });
                  } else {
                    this.$message({
                      type: "error",
                      message: "用户名或邮箱错误",
                      showClose: true,
                    });
                  }
                }
              });
            })
            .catch(() => {
              //取消操作
              this.$message({
                type: "info",
                message: "已取消密码重置",
              });
            });
        } else {
          // 表单验证错误，返回false
          console.log("error submit!!");
          return false;
        }
      });
    },
  },
  // 页面初始化
  mounted() {
    this.logincheck();
    this.canvas = document.getElementById("myCanvas");
    this.context = this.canvas.getContext("2d");
    this.createStar(true);
    this.drawFrame();
  },
};
</script>

<style scoped>
/* 页面样式 */
.rpw {
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: #e4e7ed;
  background-image: url("../../static/images/1.jpg");
}
/* 标题样式 */
.title {
  font-size: large;
  font-weight: bolder;
  text-align: center;
  color: #ffffff;
  margin-bottom: 10px;
}
/* 表单区域样式 */
.main-rpw {
  position: absolute;
  left: 48%;
  top: 40%;
  width: 320px;
  height: 270px;
  margin: -190px 0 0 -190px;
  padding: 40px;
  border-radius: 5px; /* 圆角边框 */
  background: #f2f6fc;
  box-shadow: -15px 15px 15px rgba(6, 17, 47, 0.7);
  opacity: 1;
  background: linear-gradient(
    230deg,
    rgba(53, 57, 74, 0) 0%,
    rgb(0, 0, 0) 100%
  );
}
/* el-form标签样式 */
.el-form {
  padding-top: 5%;
  padding-left: 0;
  padding-right: 10%;
  width: 300px;
}
/* el-form-item标签样式 */
.el-form-item {
  margin-left: -10%;
}
/* el-row标签样式 */
.el-row {
  height: 100%;
  width: 100%;
}
/* link标签样式 */
.link {
  margin-top: -10%;
  text-align: center;
  margin-left: 5%;
}
/* el-link标签样式 */
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
.reset_form >>> .el-form-item__label {
  color: #ffffff;
}
.reset_input >>> .el-input__inner {
  background-color: transparent;
  color: cornsilk;
}
</style>
