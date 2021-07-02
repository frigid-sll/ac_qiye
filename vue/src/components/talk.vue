<template>
    <div id="talk">
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
        <div id="da">
            <h3>
            <span class="ti">{{health}}</span>
            与
            <span class="ti">{{customer}}</span>
            的聊天记录
        </h3>
            <label>开始日期：</label><input type="date" id="start_y"/><input type="time" id="start_h"/>&nbsp;&nbsp;
            <label>结束日期：</label><input type="date" id="end_y"/><input type="time" id="end_h"/>
            <button @click="find()">查询</button>
        </div>
        <br><br>

        <div id="t">
            <div v-for="(item,index) in res_msg">
            
                <div v-if="send[index]==health" >
                    <div class="health_name"><br>{{send[index].slice(0,3)}}</div>
                    <div class="health_detail">
                        <span class="health_content">
                            <span v-if="msg_type[index]=='image' || msg_type[index]=='emotion'">
                                <span v-if="item.includes('群发消息')">
                                    <img  :src="item.slice(0,item.indexOf('(群发消息'))"  width="200px"><br>
                                    <b style="color:red;">{{item.slice(item.indexOf('(群发消息'),item.length)}}</b>
                                </span>
                                <img v-else="item.includes('群发消息')" :src="item"  width="200px">
                            </span>
                            <span v-if="msg_type[index]=='text' || msg_type[index]=='location' || msg_type[index]=='revoke' || msg_type[index]=='weapp'">
                                <span v-if="item.includes('群发消息')">
                                    {{item.slice(0,item.indexOf('(群发消息'))}}<br>
                                    <b style="color:red;">{{item.slice(item.indexOf('(群发消息'),item.length)}}</b>
                                </span>
                                <span v-else="item.includes('群发消息')">
                                    {{item}}
                                </span>
                            </span>
                            <!-- file -->
                            <span v-if="msg_type[index]=='file'">
                                <span v-if="item.includes('群发消息')">
                                    <a class="down" title="点击下载" :href="item.slice(0,item.indexOf('(群发消息'))">
                                        {{item.slice(item.indexOf('(static/')+14,item.length)}}
                                    </a>
                                    <br>
                                    <b style="color:red;">{{item.slice(item.indexOf('(static/')+14,item.length)}}</b>
                                </span>
                                <span v-else="item.includes('群发消息')">
                                    <a class="down" title="点击下载" :href="item">
                                        {{item.slice(item.indexOf('(static/')+14,item.length)}}
                                    </a>
                                </span>
                            </span>
                            <!-- file -->
                        </span> 
                        <br>
                        <span class="health_time">{{msgtime[index]}}</span>
                    </div>
                </div>

                <div  v-if="send[index]==customer">
                    <div  class="customer_name"><br>{{send[index].slice(0,3)}}</div>
                    <div class="customer_detail">
                        <span class="customer_content">
                            <span v-if="msg_type[index]=='image' || msg_type[index]=='emotion'">
                                <span v-if="item.includes('群发消息')">
                                    <img  :src="item.slice(0,item.indexOf('(群发消息'))"  width="200px"><br>
                                    <b style="color:red;">{{item.slice(item.indexOf('(群发消息'),item.length)}}</b>
                                </span>
                                <img v-else="item.includes('群发消息')" :src="item"  width="200px">
                            </span>

                            <span v-if="msg_type[index]=='text' || msg_type[index]=='location' || msg_type[index]=='revoke' || msg_type[index]=='weapp'">
                                <span v-if="item.includes('群发消息')">
                                    {{item.slice(0,item.indexOf('(群发消息'))}}<br>
                                    <b style="color:red;">{{item.slice(item.indexOf('(群发消息'),item.length)}}</b>
                                </span>
                                <span v-else="item.includes('群发消息')">
                                    {{item}}
                                </span>
                            </span>

                            <!-- file -->
                            <span v-if="msg_type[index]=='file'">
                                <span v-if="item.includes('群发消息')">
                                    <a class="down"  title="点击下载" :href="item.slice(0,item.indexOf('(群发消息'))">
                                        {{item.slice(0,item.indexOf('(群发消息'))}}
                                    </a>
                                    <br>
                                    <b style="color:red;">{{item.slice(item.indexOf('(static/')+14,item.length)}}</b>
                                </span>
                                <span v-else="item.includes('群发消息')">
                                    <a class="down" title="点击下载" :href="item">
                                        {{item.slice(item.indexOf('(static/')+14,item.length)}}
                                    </a>
                                </span>
                            </span>
                            <!-- file -->
                        </span>
                        <br>
                        <span class="customer_time">{{msgtime[index]}}</span>
                    </div>
                </div>
                     
                <br>
            </div>
        </div>
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
            customer:'',
            res_msg:'',
            send:'',
            msgtime:'',
            start_y:'',
            start_h:'',
            end_y:'',
            end_h:'',
            msg_type:'',
        }
    },
    computed:{
        _get:function(){
            this.health=this.$route.query.h
            this.customer=this.$route.query.c
            this.axios.post('/api/ac_talk/',
					Qs.stringify({  
                        health: this.health,
                        customer:this.customer,
                        start_y:this.start_y,
                        start_h:this.start_h,
                        end_y:this.end_y,
                        end_h:this.end_h
            		}),
					).then((res)=>{
						if(res.data.code==200){
                            this.send=res.data.send
                            this.res_msg=res.data.res_msg
                            this.msgtime=res.data.res_time
                            this.msg_type=res.data.msgtype
						}		
					})
        }
    },
    methods:{
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
        find:function(){
            this.start_y=document.getElementById('start_y').value
            this.start_h=document.getElementById('start_h').value
            this.end_y=document.getElementById('end_y').value
            this.end_h=document.getElementById('end_h').value
            if(this.start_y&&this.start_h&&this.end_y&&this.end_h){
                this.axios.post('/api/ac_talk/',
					Qs.stringify({  
                        health: this.health,
                        customer:this.customer,
                        start_y:this.start_y,
                        start_h:this.start_h,
                        end_y:this.end_y,
                        end_h:this.end_h
            		}),
					).then((res)=>{
						if(res.data.code==200){
                            this.send=res.data.send
                            this.res_msg=res.data.res_msg
                            this.msgtime=res.data.res_time
						}
                        if(res.data.code==100){
							alert('无内容')
						}	
                        if(res.data.code==0){
							alert('请输入正确的时间查询')
						}		
					})
            }else{
                alert('请输入完整的参数进行查询')
            }
            
        }
    }
}
</script>
<style scoped>
    @import "../../static/css/talk.css";
</style>