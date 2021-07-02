<template>
    <div id="relative">
        {{_get}}
        <button id="one" class="index" @click="c">
            <span class="title">获取会话内容</span>
        </button>
        <button id="two" class="index" @click="h">
            <span class="title">健康师与客户</span>
        </button>
        <button id="three" class="index" @click="hg">
            <span class="title">健康师管理</span>
        </button>
        <button id="four" class="index" @click="ct">
            <span class="title">客户管理</span>
        </button>
        <table align="center" class="b" cellpadding="20" cellspacing="0">
            <tr>
                <td >健康师呢称</td>
                <td >健康师负责的客户列表</td>
            </tr>
            <tr v-for="x in health">
                <td class="b">
                    {{x.name}}
                </td>
                <td align="right" class="b">
                    <div v-for="y,i in x.customer" style="display:inline">
                        <a title="点击查看聊天记录" @click="s(x.name,y)">
                            <button class="c"><span class="a">{{y}}</span></button>&nbsp;&nbsp;
                            <span v-if="(i+1)%3==0"><br><br></span>
                        </a>
                    </div>
                </td>
            </tr>
        </table>
        <div id="bc"></div>
    </div>
</template>
<script>
//# sourceMappingURL=file.js.map
import Qs from 'qs'
export default {
    data(){
        return{
            health:'',
        }
    },
    computed:{
        _get:function(){
            this.axios.get('/api/ac_health/').then((res)=>{
                if(res.data.code==200){
                    this.health=res.data.health
                    // alert('请求成功')
                }else{
                    alert('请求失败')
                }
                })
        }
    },
    methods:{
        hg:function(){
            this.$router.push({
                path:'/health',
                query:{
                }
            })
        },
        h:function(){
            location.reload();
        },
        c:function(){
            this.$router.push({
                path:'/',
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
        s:function(h,c){
            this.$router.push({
                path:'/talk',
                query:{
                    h:h,
                    c:c
                }
            })
        }
    }
}
</script>
<style scoped>
    .a{
        color:#D7634F;
        text-decoration:underline ;
    }
    .b{
        box-shadow: 1px 1px 10px pink;
    }
    .c{
        height: 30px;
        border: 0px;
        background:#F1F3F4;
    }
</style>