<template>
  <div class="main">
    <el-container>
      <el-header>
        <div class="logo" @click="toIndex">
          <img src="/static/images/logo.png" class="logoImg" />
          <span class="title">VDSurvey</span>
          <span class="subtitle">——免费的在线问卷调查系统</span>
        </div>
        <div class="lrcontainer">
          <!-- 未登录时显示-->
          <template v-if="!showname">
            <el-button
              plain
              style="font-size: 15px"
              type="primary"
              @click="toLogin"
              >登录</el-button
            >
            <el-button plain style="font-size: 15px" @click="toRegister"
              >注册</el-button
            >
          </template>
          <!-- 登录时显示-->
          <template v-else>
            <!-- 登录成功，显示用户名 -->
            <el-dropdown trigger="click" @command="handleCommand">
              <span class="el-dropdown-link">
                {{ username }}<i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <!-- 退出登录 -->
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="a">问卷管理</el-dropdown-item>
                <el-dropdown-item command="b">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </template>
        </div>
      </el-header>
      <el-main style="padding: 0">
        <router-view @state="state" />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { designOpera } from "./api";
export default {
  name: "Base",
  data: function () {
    return {
      showname: false, // 登录、注册按钮的显示
      username: "", // 用户名
    };
  },
  methods: {
    toIndex() {
      this.$router.push({ path: "/index" });
    },
    toLogin() {
      this.$router.push({ path: "/login" });
    },
    toRegister() {
      this.$router.push({ path: "/register" });
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
        }
        this.state(); // 调用state方法
      });
    },
    toHome() {
      this.$router.push({ path: "/home" });
    },
    //判断session中是否存在数据，存在将showname置为true，否则false
    state() {
      console.log("state");
      console.log(sessionStorage.getItem("username"));
      if (sessionStorage.getItem("username") != null) {
        this.showname = true;
        this.username = sessionStorage.getItem("username");
      } else {
        this.showname = false;
      }
    },
    //下拉菜单操作
    handleCommand(command) {
      if (command == "a") {
        this.toHome();
      } else if (command == "b") {
        this.exit();
      }
    },
    //登出
    exit(command) {
      designOpera({
        opera_type: "exit", // 操作类型
        username: sessionStorage.getItem("username"), //获取session中的用户名
      }).then((data) => {
        console.log(data);
        if (data.code == 0) {
          sessionStorage.clear(); //登出成功，清空session
          this.state(); // 调用state方法
          this.toLogin(); // 调用toLogin方法
        } else {
          this.$message({
            // 报错友好提示
            type: "error",
            message: "网络错误！",
            showClose: true,
          });
        }
      });
    },
  },
  // 页面初始化
  mounted() {
    this.logincheck();
  },
};
</script>

<style scoped>
.main {
  position: absolute;
  width: 100%;
  height: 100%;
  /* background-color: #FFFFCC; */
}
.logoImg {
  width: 30px;
  vertical-align: middle;
}
.logo {
  position: absolute;
  left: 100px;
  height: 60px;
  display: inline-block;
  /* background-color: #409eff; */
  line-height: 60px;
  font-size: 20px;
  color: antiquewhite;
  cursor: pointer;
}
.title {
  color: floralwhite;
}
.subtitle {
  font-size: 13px;
  margin-left: 5px;
  color: floralwhite;
}
.lrcontainer {
  float: right;
  margin-right: 50px;
  line-height: 60px;
}
.el-header {
  /* border-bottom: 2px solid #409eff; */
  background-color: #2e3e4e;
}
.el-dropdown-link {
  cursor: pointer;
  color: #409eff;
}
.el-icon-arrow-down {
  font-size: 12px;
}
</style>