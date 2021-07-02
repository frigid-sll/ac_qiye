<template>
    <div id="ac_content">
        <button id="one" class="index" @click="c" >
            <span class="title">获取会话内容</span>
        </button>
        <button id="two" class="index" @click="h" >
            <span class="title">健康师与客户</span>
        </button>
        <button id="three" class="index" @click="hg"  >
            <span class="title">健康师管理</span>
        </button>
        <button id="four" class="index" @click="ct" >
            <span class="title">客户管理</span>
        </button>

        <button id="a" class="index" @click="_get"  >点击获取最新内容</button>
        <br>
        <span v-if="ip">请添加此ip:{{ip}}</span>
        <span v-if="add">请在数据库添加这些信息:{{add}}</span>
        <br>
        <div id="bc"></div>
    </div>
</template>
<script>
//# sourceMappingURL=file.js.map
import Qs from 'qs'
export default {
    data(){
        return{
            ip:'',
            add:'',
        }
    },
    methods:{
        _get:function(){
            this.is_solve=false
            document.getElementById("a").disabled=true;
            this.ip=''
            this.add=''
            this.axios.get('/api/ac_content/').then((res)=>{
                if(res.data.code==200){
                    this.ip=''
                    alert('请求成功')
                    this.add=res.data.add
                    document.getElementById("a").disabled=false;
                }
                if(res.data.code==0){
                    alert('请加入ip后请求')
                    this.ip=res.data.ip
                    document.getElementById("a").disabled=false;
                }
                if(res.data.code==100){
                    alert('没有新的内容拉取')
                    document.getElementById("a").disabled=false;
                }
                })
        },
        h:function(){
            this.$router.push({
                path:'/relative',
                query:{
                }
            })
        },
        c:function(){
            location.reload();
        },
        hg:function(){
            this.$router.push({
                path:'/health',
                query:{
                }
            })
        },
        ct:function(){
            this.$router.push({
                path:'/customer',
                query:{
                }
            })
        },
    }
}
</script>
