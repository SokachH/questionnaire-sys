<template>
  <div class="login">
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
            >
              <i class="el-icon-user" slot="prefix"> </i>
            </el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              @keyup.enter.native="login('loginForm')"
              placeholder="请输入密码"
              v-model="loginForm.password"
              show-password
            >
              <i class="el-icon-lock" slot="prefix"> </i>
            </el-input>
          </el-form-item>
          <!-- 登录按钮 -->
          <el-form-item>
            <el-button
              type="primary"
              @click="login('loginForm')"
              style="text-align: center; width: 150px"
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
export default {
  name: "Login",
  data() {
    return {
      // 表单数据
      loginForm: {
        username: "", //用户名
        password: "", //密码
      },
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
      },
    };
  },
  //页面初始化
  mounted() {
    this.logincheck();
  },
  methods: {
    //检查登录是否过期
      logincheck(){
          designOpera({
          opera_type:'logincheck',
        })
        .then(data=>{
          console.log(data);
          if(data.code==404){
            this.$router.push({path:'/login'})
          }
          if(data.data!=null){
            console.log(data)
            sessionStorage.setItem('username',data.data.user) //将后端传的username存入session
            this.$router.push({path:'/home'})
          }
        })
      },
    //登录方法
    login(formName) {
      // 表单验证通过，可进行操作
      this.$refs[formName].validate((valid) => {
        if (valid) {
          designOpera({
            opera_type:'login',  //操作类型
            username:this.loginForm.username,  //用户名
            password:this.$md5(this.loginForm.password),  //密码md5加密
          })
            .then(data=>{
              console.log(data, "hihi");
              if (data.code==0) {  //登录成功，并提示
                this.$notify({
                  type: 'success',
                  message: '欢迎你,' + this.loginForm.username + '!',
                  duration: 3000
                });
                this.$router.push({path:'/home'});  //跳转到用户主页面
                sessionStorage.setItem("username",this.loginForm.username)   //将用户名存入session中
                this.$emit("state");  //将状态传到base页面
              }
              else {
                if(data.code==-5){  //未注册,友好提示未注册
                    this.$message({
                    type: 'error',
                    message: '您还未注册账户，请注册',
                    showClose: true
                  });
                }
                else { //账号或密码错误提示
                    this.$message({
                    type: 'error',
                    message: '账号或密码错误',
                    showClose: true
                  });
                }
              }
            })
        } else {
          return false;  //表单验证错误返回false
        }
      })
    },
  }
};
</script>


<style scoped>
  .login {
    position: absolute;
    width:100%;
    height:100%;
    background-color: #E4E7ED;
  }
  .title {
    font-size: large;
    font-weight: bolder;
    text-align: center;
    color:black;
  }
  .main_login {
    position: absolute;
    left:48%;
    top:40%;
    width:320px;
    height:250px;
    margin:-190px 0 0 -190px;
    padding:40px;
    border-radius: 5px;
    background: #F2F6FC;
  }
  .el-form {
    padding-top: 5%;
    padding-left: 10%;
    padding-right: 10%;
    width:280px;
  }
  .el-row {
    height: 100%;
    width: 100%;
  }
  .link{
    margin-top: -13%;
    text-align: center;
    margin-left: -5%;
  }
  .el-link{
    margin-left: 8px;
    line-height: 20px;
    font-size: 8px;
  }
</style>
