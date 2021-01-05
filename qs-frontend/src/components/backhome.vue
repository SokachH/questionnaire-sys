
<template>
  <div class="backhome">
    <el-row>
      <el-col>
        <!--标签页-->
         <el-tabs type="border-card" v-model="activeName">
            <el-tab-pane label="问卷管理" name="wjgl">           
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
                    <el-tabs  v-model="activeName">
                        <div class="content">
                            <div v-show="nowSelect.id==0||nowSelect.id==null">请先选择问卷</div>
                            <design ref="design" v-show="nowSelect.id!=0&&nowSelect.id!=null"></design>
                        </div>
                    </el-tabs>
                </el-col>
              
            </el-tab-pane>
            <el-tab-pane label="用户管理" name="hdtj">
              
            </el-tab-pane>
          </el-tabs>
      </el-col>
    </el-row>
  </div>
</template>
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
        activeName:'wjgl',//标签页当前选择项
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
      

      //检查登录是否过期
      logincheck(){
          designOpera({
          opera_type:'logincheck',
        })
        .then(data=>{
          console.log(data);
          if(data.code==404){//如果返回的错误是404，跳转到登录页面
            this.$message({
              type: 'error',
              message: '您还未登录，请登录',
              showClose: true
            });
            this.$router.push({path:'/login'})
          }
          else{
            this.getWjList();
            this.getUsersList();
          }
        })
      },
      //获取问卷列表
      getWjList(){
        this.loading=true;
        designOpera({
          opera_type:'get_wj_list',
          username: this.input,
        })
          .then(data=>{
            console.log(data);
            this.wjList=data.data.detail;
            this.loading=false;
            //获取当前选中问卷题目
            this.lookDetail();
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
          opera_type:'delete_wj',
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
