<template>
  <div class="main">
    <el-container>
      <el-header>
        <div class="logo" @click="toIndex">
          <!-- <img src=""> -->
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
          <template v-else></template>
        </div>
      </el-header>
      <el-main style="padding: 0">
        <router-view />
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
      this.$router.push({ path: "/login" });
    },
    toRegister() {
      this.$router.push({ path: "/register" });
    },
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
  color:floralwhite;
}
.subtitle {
  font-size: 13px;
  margin-left: 5px;
  color:floralwhite;
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
</style>