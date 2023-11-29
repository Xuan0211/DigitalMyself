<template>
  <div class="flex-col justify-start items-center page">
    <div class="flex-row section">
      <div class="flex-col group">
        <div class="flex-col">
          <div class="self-center group_top">
            <span class="text">
              Welcome to
              <br />
            </span>
            <span class="text_LOGO">DigitalMyself</span>
          </div>
          <div class="self-stretch divider"></div>
          <div class="flex-row items-center self-stretch option_group" v-for="option, index in optionList" :key="index">
            <img class="option_image" :src="option.imgUrl" />
            <span class="ml-16 option_font">{{ option.label }}</span>
          </div>
        </div>
        <div class="flex-col items-center group_bottom">
          <span class="text_CN">数字飞升 拯救自己</span>
          <span class="text_EN">Designed Dy Xuan</span>
        </div>
      </div>
      <div class="flex-col group_left">
        <div class="flex-col section_chat">
          <div class="flex-row msg_group" v-for="msg, index in msgList" :key="index">
            <img v-if="msg.label === 'bot'" class="image" :src="bot.avatarUrl" />
            <div class="flex-col justify-start text-wrapper"
              :style="{ backgroundColor: msg.label === 'bot' ? '#1862991a' : '#f7e27933' }">
              <span class="font_msg">{{ msg.msg }}</span>
            </div>
            <img v-if="msg.label === 'user'" class="image" :src="bot.avatarUrl" />
          </div>
        </div>
        <div class="flex-col justify-start items-end section_input">
          <el-input type="textarea" v-model="input" rows="4" maxlength="30"></el-input>
          <div class="flex-col justify-start items-center button" @click="send">
            <span class="text_send">发送</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
import { sendMsg } from '@/api/request.js'
export default {
  name: "MainPage",
  components: {},
  props: {},
  data() {
    return {
      msgList: [
        {
          label: "bot",
          msg: "我是DigitalMyself，请问有什么可以帮助您的？"
        },
        {
          label: "user",
          msg: "上节软工课讲了啥？"
        }
      ],
      optionList: [
        {
          imgUrl: "https://ide.code.fun/api/image?token=6566083efcfbac001135915e&name=e98755040e3a9a51b113036a48c0c375.png",
          label: "数据导入"
        },
        {
          imgUrl: "https://ide.code.fun/api/image?token=6566083efcfbac001135915e&name=5647a48d4450dec3c745af4a247fe327.png",
          label: "数据管理"
        },
        {
          imgUrl: "https://ide.code.fun/api/image?token=6566083efcfbac001135915e&name=65d25cf15f3820a2eb559b19239d640c.png",
          label: "设置"
        }
      ],
      bot: {
        avatarUrl: "https://ide.code.fun/api/image?token=6566083efcfbac001135915e&name=acb51f6a8b7b53b8800cc8d75318c662.png"
      },
      input: undefined
    };
  },

  methods: {
    send() {
      this.msgList.push(
        {
          label: "user",
          msg: this.input
        }
      );
      sendMsg(this.input).then(res => {
        console.log(res)
        this.msgList.push(
          {
            label: "bot",
            msg: res.ans
          });
        this.input = undefined;
      })
        .catch(err => {
          console.log("err")
        });
      console.log("msg end:" + this.input);
    }
  },
};
</script>
<style scoped lang="css">
.page {
  padding: 12rem 0 13.81rem;
  background-image: url(https://codefun-proj-user-res-1256085488.cos.ap-guangzhou.myqcloud.com/62f8bcea5a7e3f03100a0ed5/62f8bd5e689f2800114ed71c/17011855686541328415.png);
  background-size: 100% 100%;
  background-repeat: no-repeat;
  width: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  height: 100%;
}

.section {
  background-color: #ffffff;
  border-radius: 0.63rem;
  filter: drop-shadow(0rem 0rem 1.56rem #00000040);
}

.group {
  padding-top: 0.63rem;
  overflow: hidden;
  width: 11.63rem;
  height: 26.19rem;
  border-right: solid 0.063rem #0000001a;
}

.group_top {
  line-height: 1.38rem;
  width: 7.63rem;
}

.text {
  color: #186299;
  font-size: 0.88rem;
  font-family: Noto Sans SC;
  font-weight: 700;
  line-height: 1.38rem;
}

.text_LOGO {
  color: #186299;
  font-size: 1.19rem;
  font-family: Noto Sans SC;
  font-weight: 700;
  line-height: 1.38rem;
}

.divider {
  margin-top: 0.63rem;
  background-color: #e4e7ed;
  height: 0.063rem;
}

.option_group {
  margin-top: 0.19rem;
  padding: 0.25rem 0.81rem;
  overflow: hidden;
  border-bottom: solid 0.063rem #0000001a;
  margin-top: 0.25rem;
}

.option_image {
  width: 1.5rem;
  height: 1.5rem;
  margin-right: 0.5rem;
}

.option_font {
  color: #000;
  font-family: Noto Sans SC;
  font-size: 11px;
  font-style: normal;
  font-weight: 400;
  line-height: 22px;
  /* 200% */
}

.group_bottom {
  padding-bottom: 0.5rem;
  margin-top: 13.5rem;
}

.text_CN {
  color: #000000;
  font-size: 0.5rem;
  font-family: Microsoft Himalaya;
  line-height: 0.46rem;
  letter-spacing: 0.22rem;
}

.text_EN {
  color: #000000;
  font-size: 0.63rem;
  font-family: Microsoft Himalaya;
  line-height: 0.38rem;
  margin-top: 0.31rem;
}

.group_left {
  overflow: hidden;
  width: 25.5rem;
  height: 26.19rem;
}

.section_chat {
  height: 18rem;
  background-image: url(https://codefun-proj-user-res-1256085488.cos.ap-guangzhou.myqcloud.com/62f8bcea5a7e3f03100a0ed5/62f8bd5e689f2800114ed71c/16827623392164512850.png);
  background-size: 100% 100%;
  background-repeat: no-repeat;
  padding: 1rem 1.5rem;
  overflow-x: scroll;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.image {
  border-radius: 0.25rem;
  width: 1.7rem;
  height: 1.81rem;
}

.text-wrapper {
  padding: 0.5rem 0 0.38rem;
  background-color: #1862991a;
  border-radius: 0.63rem;
  width: 20rem;
  margin-left: 0.3rem;
  margin-right: 0.3rem;
}

.msg_group {
  margin: 0.2rem 0;
}

.font_msg {
  font-size: 0.63rem;
  font-family: Microsoft YaHei;
  line-height: 0.64rem;
  color: #000000;
  margin: 0 1.25rem;
  line-height: 0.68rem;
  text-align: left;
}

.section_input {
  background-color: #ffffff;
  overflow: hidden;
  border-top: solid 0.063rem #0000000d;
  position: relative;
  bottom: 0;
  height: 8rem;
}

.button {
  margin-right: 0.75rem;
  margin-top: 0.5rem;
  padding: 0.38rem 0;
  background-color: #186299;
  border-radius: 0.25rem;
  width: 3.38rem;
}


.text_send {
  color: #ffffff;
  font-size: 0.75rem;
  font-family: Noto Sans SC;
  font-weight: 700;
  line-height: 0.71rem;
}
</style>