<template>
    <div id="health">
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

        <button class="handle index" @click="handle('增加')">增</button><br><br>
        <button  class="handle index" @click="handle('删除')">删</button><br><br>
        <button  class="handle index" @click="handle('修改')">改</button><br><br>
        <button  class="handle index" @click="handle('查询')">查</button><br><br>
        <h3>健康师列表</h3>

        <ul style="list-style-type:none" id="all_content">
            <li v-for="x in health_list" class="li">
                <!-- <input type="submit" :value="x.name" disabled="disabled" class="show index"><br> -->
                <span class="show index" style="line-height:28px">{{x.name}}</span><br>
            </li>
        </ul>
        <span id="chaxun"></span>
        <div id="editor" style="display:none">
            <span id="xiugai" style="display:none">请输入修改后的呢称：</span>
            <input id="edit" class="form-control" type="text" value="">
            <input id="content" value="" type="submit" class="form-control" @click="result">
            <input id="xiugaianniu" value="提交" type="submit" class="form-control" @click="xiugaicaozuo" style="display:none">
            <br>
        </div>
        <div id="bc"></div>
    </div>
</template>
<script>
//# sourceMappingURL=file.js.map
import "@/../static/css/navigation.css"
import Qs from 'qs'
export default {
    data(){
        return{
            health_list:'',
            msg:'',
            msgtype:'',
            zeng:'',
            shan:'',
            gai:'',
            cha:'',
            gai_res:'',
        }
    },
    computed:{
        _get:function(){
            this.axios.get('/api/ac_health/').then((res)=>{
                if(res.data.code==200){
                    this.health_list=res.data.health
                }
                })
        }
    },
    methods:{
        xiugaicaozuo:function(){
            this.gai_res=document.getElementById('edit').value
            if(this.gai_res){
                this.axios.post('/api/gai_health/',
					Qs.stringify({  
                        gai_ever:this.msg,
                        gai_res: this.gai_res,
            		}),
					).then((res)=>{
						if(res.data.code==200){
                            alert('修改成功')
                            parent.location.reload()
						}
					})
            }else{
                alert('修改失败')
                parent.location.reload()
            }
        },
        h:function(){
            this.$router.push({
                path:'/relative',
                query:{
                }
            })
        },
        c:function(){
            this.$router.push({
                path:'/',
                query:{
                }
            })
        },
        hg:function(){
            location.reload();
        },
        ct:function(){
            this.$router.push({
                path:'/customer',
                query:{
                }
            })
        },
        handle:function(v){
            document.getElementById('editor').style.display='block'
            document.getElementById('content').value=v
            document.getElementById('all_content').style.display='block'
            document.getElementById('edit').value=''
            document.getElementById('chaxun').style.display='none'

        },
        result:function(){
            this.msgtype=document.getElementById('content').value
            this.msg=document.getElementById('edit').value
            document.getElementById('edit').value=''
            if(this.msg){
                this.axios.post('/api/handle_health/',
					Qs.stringify({  
                        msg:this.msg,
                        msgtype:this.msgtype,
            		}),
					).then((res)=>{
						if(res.data.code==200){
                            this.zeng=res.data.zeng
                            this.shan=res.data.shan
                            this.gai=res.data.gai
                            this.cha=res.data.cha
                            if(this.cha){
                                document.getElementById('all_content').style.display='none'
                                document.getElementById('chaxun').style.display='block'
                                document.getElementById('chaxun').innerHTML=this.cha
                            }
                            if(this.shan){
                                alert('删除成功')
                                parent.location.reload()
                            }
                            if(this.zeng){
                                alert('添加成功')
                                parent.location.reload()
                            }
                            if(this.gai){
                                document.getElementById('xiugai').style.display='inline'
                                document.getElementById('xiugaianniu').style.display='inline'
                                document.getElementById('content').style.display='none'
                                // alert('修改成功')
                                // parent.location.reload()
                            }
						}else{
                            alert('fail')
                        }		
					})
            }else{
                            alert('请输入完整参数')
                        }	
        }
    }
}
</script>

<style scoped>
    @import "../../static/css/bootstrap.min.css"; 
    @import "../../static/css/health.css"; 
</style>