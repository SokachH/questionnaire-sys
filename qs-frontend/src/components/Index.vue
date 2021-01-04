<template>
  <div class="main">
    <el-carousel :interval="4000" height="400px">
      <el-carousel-item v-for="(item, index) in imgs" :key="index">
        <img :src="item.url" style="width: 100%; height: 100%" />
        <div class="cover">
          {{ item.title }}<br />
          <span style="font-size: 35px">{{ item.subTitle }}</span>
        </div>
        <!-- <h3 class="medium">{{ item }}</h3> -->
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script>
export default {
  data() {
    return {
      imgs: [
        {
          title: "免费在线问卷调查系统",
          subTitle: "Free Online Questionnaire System",
          url: "/static/images/2.jpg"
        },
        {
          title: "简单的打开方式",
          subTitle: "Simple Opening Method",
          url: "/static/images/2.jpg"
        },
        {
          title: "多样的数据可视化",
          subTitle: "Diversified data visualization",
          url: "/static/images/2.jpg"
        },
      ]
    }
  }
};
</script>

<style scoped>
.main {
  position: relative;
  width: 100%;
  height: 100%;
}
.cover {
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  z-index: 100;
  left: 0;
  top: 0;
  color: white;
  font-size: 50px;
  line-height: 60px;
  padding-top: 150px;
}
</style>