<template>
  <div class="main">
    <el-container>
      <el-header>
        <div class="logo">
          <!-- <img src=""> -->
          <!-- <span @click="toIndex">在线问卷系统</span> -->
          <el-button type="info" @click="toIndex">在线问卷系统</el-button>
          <span>xxxxxxxxxxx</span>
          <el-button type="primary" @click="toLogin">登录</el-button>
          <el-button type="success" @click="toRegister">注册</el-button>
        </div>
      </el-header>
      <el-main>
        <router-view/>
      </el-main>
    </el-container>
  </div>
</template>

<script>
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
      this.$router.push({path: "/login"});
    },
    toRegister() {
      this.$router.push({path: "/register"});
    }
  },
};
</script>

<style scoped>
.main {
  position: absolute;
  width: 100%;
  height: 100%;
}
.logo {
  background-color: #409eff;
}
.el-header {
  border-bottom: 2px solid #409eff;
  background-color: white;
}
</style>