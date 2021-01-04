<!--
程序名：问卷设计主页面
功能：对问卷进行设计
-->
<template>
  <div class="home">
    <el-row>
      <el-col :span="6">
        <!--操作栏-->
        <div class="opera">
          <el-tooltip class="item" effect="dark" content="创建问卷" placement="bottom">
            <el-button icon="el-icon-plus" type="text" class="rightButton" @click="addWjButtonClick"></el-button>
          </el-tooltip>
          <el-tooltip class="item" effect="dark" content="编辑问卷" placement="bottom">
            <el-button icon="el-icon-edit" type="text" class="rightButton" @click="editWj" :disabled="nowSelect.id==0||nowSelect.id==null"></el-button>
          </el-tooltip>
          <el-tooltip class="item" effect="dark" :content="nowSelect.status==0?'发布问卷':'暂停问卷'" placement="bottom" >
            <el-button :icon="nowSelect.status==0?'el-icon-video-play':'el-icon-video-pause'"  type="text" class="rightButton" @click="pushWj" :disabled="nowSelect.id==0||nowSelect.id==null"></el-button>
          </el-tooltip>
          <el-tooltip class="item" effect="dark" content="预览问卷" placement="bottom">
            <el-button icon="el-icon-view" type="text" class="rightButton" @click="previewWj" :disabled="nowSelect.id==0||nowSelect.id==null"></el-button>
          </el-tooltip>
          <el-tooltip class="item" effect="dark" content="删除问卷" placement="bottom">
            <el-button icon="el-icon-delete" type="text" class="rightButton" @click="deleteWj" :disabled="nowSelect.id==0||nowSelect.id==null"></el-button>
          </el-tooltip>
          <el-tooltip class="item" effect="dark" content="分享问卷" placement="bottom">
            <el-button icon="el-icon-share" type="text"class="rightButton" @click="shareWj" :disabled="nowSelect.id==0||nowSelect.id==null"></el-button>
          </el-tooltip>
          <!--<el-tooltip class="item" effect="dark" content="添加模板库" placement="bottom">-->
            <!--<el-button icon="el-icon-upload" type="text"class="rightButton" @click="addTemp"></el-button>-->
          <!--</el-tooltip>-->
        </div>

        <!--左侧导航栏-->
        <el-menu :default-active="defaultActive.toString()" v-loading="loading" class="menu">
          <!--问卷列表-->
          <div style="width:100%;text-align: center;font-size: 15px;line-height: 20px;margin-top: 20px;color: #303133" v-if="nowSelect.id==0||nowSelect.id==null">
            点击上方&nbsp;+&nbsp;创建第一个问卷
          </div>
          <el-menu-item v-for="(item,index) in wjList" :index="(index+1).toString()" @click="wjClick(item.id,index)">
            <i class="el-icon-tickets"></i>
            <span slot="title" style="display: inline-block">
              {{item.title}}
              <span style="color: #F56C6C;font-size: 13px;" v-if="item.status==0">
                <i class="el-icon-link" style="margin:0;font-size: 13px;color: #F56C6C;width:10px;"></i>
                未发布
              </span>
              <span style="color: #67C23A;font-size: 13px;" v-if="item.status==1">
                <i class="el-icon-link" style="margin:0;font-size: 13px;color: #67C23A;width:10px;"></i>
                已发布
              </span>
            </span>
          </el-menu-item>
        </el-menu>
      </el-col>

      <el-col :span="18">
        <!--标签页-->
         <el-tabs type="border-card" v-model="activeName">
            <el-tab-pane label="问卷设计" name="wjsj">
              <!--内容区域-->
              <div class="content">
                <div v-show="nowSelect.id==0||nowSelect.id==null">请先选择问卷</div>
                <design ref="design" v-show="nowSelect.id!=0&&nowSelect.id!=null"></design>
              </div>
            </el-tab-pane>
            <el-tab-pane label="回答统计" name="hdtj">
              <div class="content" ref="pdf">
                <div v-show="nowSelect.id==0||nowSelect.id==null">请先选择问卷</div>
                <data-show ref="dataShow" v-show="nowSelect.id!=0&&nowSelect.id!=null"></data-show>
              </div>
            </el-tab-pane>
          </el-tabs>
      </el-col>
    </el-row>

    <!--添加问卷弹窗-->
    <el-dialog title="添加问卷" :visible.sync="dialogShow" :close-on-click-modal="false" class="dialog">
      <el-form ref="form" :model="willAddWj" label-width="80px">
        <el-form-item label="问卷标题" style="width: 100%;" required>
          <el-input v-model="willAddWj.title" placeholder="请输入问卷标题" ></el-input>
        </el-form-item>
        <el-form-item label="问卷描述" style="width: 100%;">
          <el-input v-model="willAddWj.desc" type="textarea" placeholder="请输入问卷描述" rows="5"></el-input>
        </el-form-item>
      </el-form>
      <div style="width: 100%;text-align: right">
        <el-button style="margin-left: 10px;" @click="openTemp">从模板库创建</el-button>
        <el-button style="margin-left: 10px;" @click="dialogShow=false">取消</el-button>
        <el-button type="primary" style="margin-left: 10px;" @click="addWj">确定</el-button>
      </div>
    </el-dialog>



    <!--模板库弹窗-->
    <el-dialog title="模板库" :visible.sync="tempDialog" :close-on-click-modal="false" class="dialog">
      <el-input placeholder="请输入关键词搜索" prefix-icon="el-icon-search" v-model="tempSearchText"></el-input>
     <el-table :data="tempData" style="width: 100%;" v-loading="tempLoading" element-loading-text="加载中...">
      <el-table-column prop="tempname" label="模板名" width="250"></el-table-column>
      <el-table-column prop="username" label="创建者"></el-table-column>
       <el-table-column label="预览">
       <el-link slot-scope="scope" type="primary" @click="lookTempWj(scope.row)">预览</el-link>
     </el-table-column>
     <el-table-column label="操作">
        <el-link slot-scope="scope" type="primary" @click="useTemp(scope.row)">使用此模板</el-link>
     </el-table-column>
    </el-table>
      <el-pagination layout="prev, pager, next" :total="tempDataCount" @current-change="changeTempPage" :page-size	="5"></el-pagination>
    </el-dialog>


    <!--分享问卷弹窗-->
    <el-dialog title="分享问卷" :visible.sync="shareDialogShow" :close-on-click-modal="true" class="dialog" @opened="makeQrcode">
      <el-form ref="form" :model="shareInfo" label-width="80px">
        <el-form-item label="问卷链接" style="width: 100%;">
          <el-row>
            <el-col :span="16">
              <el-input v-model="shareInfo.url" readonly></el-input>
            </el-col>
            <el-col :span="8">
              <el-button style="margin-left: 5px;" v-clipboard:copy="shareInfo.url" v-clipboard:success="copySuccess" v-clipboard:error="copyError">复制</el-button>
              <el-button style="margin-left: 5px;" @click="openShareUrl">打开</el-button>
            </el-col>
          </el-row>
        </el-form-item>
        <el-form-item label="二维码" style="width: 100%;">
          <canvas id="canvas" style="width: 150px;height: 150px;"></canvas>
        </el-form-item>
      </el-form>
    </el-dialog>

  </div>
</template>