
<template>
  <div class="backhome">
    <el-row>
      <el-col>
        <!--标签页-->
         <el-tabs type="border-card" v-model="activeName">
            <el-tab-pane label="问卷管理" name="wjsj">
              <!--内容区域-->             
              <el-col :span="6">
                <el-menu :default-active="defaultActive.toString()" v-loading="loading" class="menu">
                  
                <!--问卷列表-->
                <el-menu-item v-for="(item,index) in wjList" :index="(index+1).toString()" @click="wjClick(item.id,index)">
                    <i class="el-icon-tickets"></i>
                    <span slot="title" style="display: inline-block">
                    {{item.title}}
                    <span style="font-size: 13px;margin-left:70px;">
                         {{item.username}}
                    </span>
                    <span style="color: #F56C6C;font-size: 13px;margin-left:50px;" v-if="item.status==0">
                        <i class="el-icon-link" style="margin:0;font-size: 13px;color: #F56C6C;width:25px;"></i>
                        未发布
                    </span>
                   
                    <span style="color: #67C23A;font-size: 13px;margin-left:50px;" v-if="item.status==1">
                        <i class="el-icon-link" style="margin:0;font-size: 13px;color: #67C23A;width:25px;"></i>
                        已发布
                    </span>
                    <el-tooltip class="item" effect="dark" content="删除问卷" placement="bottom">
                        <el-button icon="el-icon-delete" type="text" class="rightButton" style="margin-left:15px;" @click="deleteWj" :disabled="nowSelect.id==0||nowSelect.id==null"></el-button>
                    </el-tooltip>
                    </span>
                </el-menu-item>
                </el-menu>
                </el-col>

                <el-col :span="18">
                    <!--标签页-->
                    <el-tabs  v-model="activeName">
                        <!--内容区域-->
                        <div class="content">
                            <div v-show="nowSelect.id==0||nowSelect.id==null">请先选择问卷</div>
                            <design ref="design" v-show="nowSelect.id!=0&&nowSelect.id!=null"></design>
                        </div>
                    </el-tabs>
                </el-col>
              
            </el-tab-pane>
            <el-tab-pane label="用户管理" name="hdtj">
              <div class="search">
                  <el-input v-model="mytext" placeholder="请输入要查找的用户名..." :disabled="false"/>
                  <el-button type="primary" class="rightButton" @click="searchuser"><i>搜索</i></el-button>
                </div>
              <el-row :gutter="50">
                <el-col :span="8">
                  <div class="grid-content bg-purple">用户名</div>
                  <div class="grid-content bg-purple-light" v-for="(item,index) in UserList" style="margin: 1px;">
                    {{item.username}}
                  </div>
                </el-col>
                <el-col :span="8">
                  <div class="grid-content bg-purple">邮箱</div>
                  <div class="grid-content bg-purple-light" v-for="(item,index) in UserList" style="margin: 1px;">
                    {{item.email}}
                  </div>
                </el-col>
                <el-col :span="8">
                  <div class="grid-content bg-purple">是否禁止该用户发布问卷(1为禁止)</div>
                  <div class="grid-content bg-purple-light" v-for="(item,index) in UserList" style="margin: 1px;">
                    {{item.status}}
                    <i class="el-icon-remove" style="margin-left: 100px;" @click="BanWj(item.username,item.email,item.status)"></i>
                  </div>
                </el-col>
              </el-row>
            </el-tab-pane>
          </el-tabs>
      </el-col>
    </el-row>
  </div>
</template>
<style>
.search{
            width: 30%;            
            margin: 10px auto;
            display: flex;
     
        }
        .search input{
            float: left;
            flex: 4;
            height: 30px;
            outline: none;
            border: 1px solid cadetblue;
            box-sizing: border-box;
            padding-left: 10px;
        }
        .search button{
            float: right;
            flex: 1;
            height: 30px;
            background-color: cadetblue;
            color: white;
            border-style: none;
            outline: none;
        }
        .search button i{
            font-style: normal;
        }
        .search button:hover{
            font-size: 16px;
        }
  .el-row {
    margin-bottom: 20px;
    
  }
  .el-col {
    border-radius: 4px;
  }
  .bg-purple-dark {
    background: #99a9bf;
  }
  .bg-purple {
    background: #d3dce6;
  }
  .bg-purple-light {
    background: #fbfffd;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
    line-height: 50px;
    color:#003E3E;
  }
  </style>
<script>
  import {designOpera} from './api'
  import Design from './Design.vue'
  import DataShow from './DataShow.vue'
  import ElButton from "../../node_modules/element-ui/packages/button/src/button";
  import QRCode from 'qrcode'
  export default{
    components:{
      ElButton,
      Design,
      QRCode,
      DataShow,
    },
    data(){
      return{
        defaultActive:1,//当前激活菜单
        activeName:'wjsj',//标签页当前选择项
        wjList:[],//问卷列表
        UserList:[],//用户列表
        loading:false,//是否显示加载中
        dialogShow:false,//添加问卷弹窗是否显示
        shareDialogShow:false,//分享问卷弹窗是否显示
        tempDialog:false,//模板库弹窗是否显示
//        nowTempData:[],//当前模板库页码
        tempData:[],
        tempDataCount:0,
        tempLoading:false,
        tempSearchText:'',
        mytext:'',

        willAddWj:{
          id:0,
          title:'',
          flag:0,
          desc:'感谢您能抽时间参与本次问卷，您的意见和建议就是我们前行的动力！',
        },
        shareInfo:{
          url:'',
        },

      }
    },
    mounted(){
      this.logincheck();

    },
    computed:{
      //现在选中的问卷信息
      nowSelect(){
        console.log('nowSelect update');
        let now=this.wjList[this.defaultActive-1];
        if(this.wjList.length==0){
          return {
            id:null,
            title:null,
            desc:null,
            status:null
          }
        }
        return{
          id:now.id,
          title:now.title,
          desc:now.desc,
          status:now.status
        }
      },
    },
    methods:{
      addTemp(){
        designOpera({
          opera_type:'add_temp',
          wjId:107,
        })
          .then(data=>{
            console.log(data);
          })
      },
      
      //使用问卷
      useTemp(item){
        this.tempLoading=true;
        designOpera({
          opera_type:'use_temp',
          wjId:item.tempid,
        })
          .then(data=>{
            console.log(data);
            this.tempLoading=false;
            this.$message({
              type: 'success',
              message: '使用模板成功！',
              showClose: true
            });
            this.tempDialog=false;
            this.dialogShow=false;
            this.getWjList();

          })
      },
      //打开问卷库
      openTemp(){
        this.tempDialog=true;
        this.changeTempPage(1);
//        this.getTempWjList();
      },
      //改变模板库页码
      changeTempPage(page){
        this.tempLoading=true;
        designOpera({
          opera_type:'get_temp_wj_list',
          page:page
        })
          .then(data=>{
            console.log(data);
            this.tempDataCount=data.count;
            this.tempData=data.detail;
            this.tempLoading=false;
          })
      },
      //预览模板问卷
      lookTempWj(item){
        let url=window.location.origin+"/tempdisplay/"+item.tempid;//问卷链接
        console.log(url);
        window.open(url);
      },
      //检查登录是否过期
      logincheck(){
          designOpera({
          opera_type:'admincheck',
        })
        .then(data=>{
          console.log(data);
          if(data.code==404){//如果返回的错误是404，跳转到登录页面
            this.$message({
              type: 'error',
              message: '您还未登录，请登录',
              showClose: true
            });
            this.$router.push({path:'/adminlogin'})
          }
          else{
            this.getWjList();
            this.getUsersList();
          }
        })
      },
      //发布问卷/暂停问卷
      pushWj(){
        let status=1;
        if(this.nowSelect.status==1)
            status=0;
        designOpera({
          opera_type:'push_wj',
          username:'test',
          wjId:this.nowSelect.id,
          status:status
        })
          .then(data=>{
            console.log(data);
            if(data.code==0){
              this.$message({
                type: 'success',
                message: status==1?'问卷发布成功！':'问卷暂停成功！'
              });
              this.getWjList();
            }
            else{
              this.$message({
                type: 'error',
                message: data.msg
              });
            }
          })
      },
      //分享问卷
      shareWj(){
        if(this.nowSelect.status==0){//问卷未发布
          this.$message({
            type: 'error',
            message: '请先发布问卷能分享！'
          });
          return;
        }
        this.shareInfo.url=window.location.origin+"/display/"+this.nowSelect.id;//问卷链接
        this.shareDialogShow=true;
      },
      //生成二维码
      makeQrcode(){
        var canvas=document.getElementById('canvas');
        QRCode.toCanvas(canvas,this.shareInfo.url);
      },
      //复制分享链接成功
      copySuccess(e){
        console.log(e);
        this.$message({
          type: 'success',
          message: '已复制链接到剪切板'
        });
      },
      //复制分享链接失败
      copyError(e){
        console.log(e);
        this.$message({
          type: 'error',
          message: '复制失败'
        });
      },
      //打开分享链接
      openShareUrl(){
        window.open(this.shareInfo.url);
      },
      //预览问卷
      previewWj(){
        let url=window.location.origin+"/display/"+this.nowSelect.id;//问卷链接
        console.log(url);
        window.open(url);
      },
      //编辑问卷
      editWj(){
        this.dialogShow=true;
        this.willAddWj=this.nowSelect;
      },
      //添加问卷按钮点击
      addWjButtonClick(){
        this.dialogShow=true;
        this.willAddWj={
          id:0,
          title:'',
          flag:0,
          desc:'感谢您能抽时间参与本次问卷，您的意见和建议就是我们前行的动力！',
        };
      },
      //添加问卷
      addWj(){
        if (this.willAddWj.title == ''){
          this.$message({
            type: 'error',
            message: '标题不能为空'
          });
          return;
        }
        designOpera({
          opera_type:'add_wj',
          username:'test',
          title:this.willAddWj.title,
          id:this.willAddWj.id,
          desc:this.willAddWj.desc,
        })
          .then(data=>{
            console.log(data);
            if(data.code==0){
              this.$message({
                type: 'success',
                message: '保存成功!'
              });
              this.getWjList();
            }
            else{
              this.$message({
                type: 'error',
                message: data.msg
              });
            }
          });
        this.dialogShow=false;
        this.willAddWj.title='';
      },
      //获取问卷列表
      getWjList(){
        this.loading=true;
        designOpera({
          // opera_type:'get_wj_list',
          opera_type:'admin_get_wj',
          // username: 'admin',
        })
          .then(data=>{
            console.log(data);
            this.wjList=data.data.detail;
            this.loading=false;
            //获取当前选中问卷题目
            this.lookDetail();
          })
      },
      searchuser(){
        this.loading=true;
        designOpera({
          opera_type:'search_user',
          username:this.mytext,
        })
          .then(data=>{
            console.log(data);
            this.UserList=data.data.detail;
            this.loading=false;
          })
      },
      //获取用户列表
      getUsersList(){
        this.loading=true;
        designOpera({
          opera_type:'get_users_list',
          username:'admin',
        })
        .then(data=>{
            console.log(data);
            this.UserList=data.data.detail;
            this.loading=false;
          })
      },
      //删除问卷
      BanWj(na,em,st){
        this.$confirm('确定禁止/允许'+na+'发布问卷?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.loading=true;
          designOpera({
          opera_type:'ban_wj',
          username:na,
          email:em,
          status:st
        })
          .then(data=>{
            console.log(data);
            if(data.code==0){
              this.$message({
                type: 'success',
                message: '操作成功!'
              });
              this.loading=false;
              this.getUsersList();
              this.defaultActive=1;
            }
            else{
              this.$message({
                type: 'error',
                message: data.msg
              });
            }
          })
        });
      },
      //删除问卷
      deleteWj(){
        this.$confirm('确定删除'+this.nowSelect.title+'? 删除后不可恢复！', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.loading=true;
          designOpera({
          opera_type:'admin_del_wj',
          adminname:'admin',
          id:this.nowSelect.id
        })
          .then(data=>{
            console.log(data);
            if(data.code==0){
              this.$message({
                type: 'success',
                message: '删除成功!'
              });
              this.loading=false;
              this.getWjList();
              this.defaultActive=1;
            }
            else{
              this.$message({
                type: 'error',
                message: data.msg
              });
            }
          })
        });
      },
      //问卷点击
      wjClick(id,index){
        this.defaultActive=(index+1).toString();
        this.lookDetail();
      },
      //查看问卷详情
      lookDetail(){
        this.$refs.design.init(this.nowSelect.id,this.nowSelect.title,this.nowSelect.desc);
        console.log("id=")
        console.log(this.nowSelect.id)
        this.$refs.dataShow.dataAnalysis(this.nowSelect.id);
      },
    }
  }
</script>
<style scoped>
  .home{
    position: absolute;
    width: 100%;
    height: calc(100vh - 100px);
    text-align: left;

  }
  .home .badgeItem{
    margin-top: 40px;
  }
  .content{
    padding: 20px;
    padding-right: 100px;
    height: calc(100vh - 175px);
    text-align: center;
    overflow-y: scroll;
    overflow-x: hidden;
  }
  .menu{
    background-color: white;
    height: calc(100vh - 100px);
    overflow-x: scroll;
    overflow-y: scroll;
    left: 0;
  }
  .home .opera{
    position: relative;
    background-color: #fafafa;
    text-align: center;
    height: 40px;
  }
  .home .rightButton{
    font-size: 16px;
  }
  .home .addWjDiv{
    height: 50px;line-height: 50px;text-align: center;
    border-bottom: 1px solid #eee
  }
</style>
