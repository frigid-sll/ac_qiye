<template>
    <div id="customer">
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

        <button id="five" class="index" @click="add_c">
            添加客户
        </button>
        <button id="six" class="index" @click="cha_c">
            查询客户
        </button>

        <span id="tit">客户列表</span>
        <br><br><br>
        <!-- 添加操作 -->
        <div id="add" style="display:none">
            客户呢称：<input type="text" class="index ad" id="add_cu">&nbsp;&nbsp;
            健康师呢称：
            <select id="add_he">
                <option  v-for="x in health_list"  :value="x" >{{x}}</option>
            </select>
            &nbsp;&nbsp;
            <button class="index ad" style="width:100px;height:25px" @click="add_re">添加</button>
        </div>

        <!-- 查询操作 -->
        <div id="cha" style="display:none">
            客户呢称：<input type="text" class="index ad" id="cha_cu">&nbsp;&nbsp;
            <button class="index ad" style="width:100px;height:25px" @click="cha_re">查询</button>
            <br><br>
            <div v-if="re_he">
                <input type="text" :value="cha_cu" class="content" id="ss"  disabled="disabled">
                
                <select id="i" disabled>
                    <option v-for="x in health_list" v-if="x==re_he" selected="selected" :value="x">{{x}}</option>
                    <option  v-for="x in health_list" v-if="x!=re_he"  :value="x">{{x}}</option>
                </select>
                <button class="handle" id="bian" @click="edit2(cha_cu)">编&nbsp;辑</button>
                <button class="handle"  @click="del(cha_cu,re_he)" id="shan">删&nbsp;除</button>
            </div>
        </div>

        <!-- 所有展示操作 -->
        <table cellpadding="15" cellspacing="0" id="all_">
            <tr id="head">
                <td class="b">客户呢称</td>
                <td class="b">负责的健康师</td>
                <td class="b">编辑操作</td>
                <td class="b">删除操作</td>
            </tr>

            <tr v-for="(item,key,i) in customer_list">
                <td class="b">
                    <input type="text" :value="key" class="content" :class="key" disabled="disabled" style="width:280px">
                </td>
                <td class="b" style="width:280px">
                    
                    <input type="text" :value="item" class="content" :class="key" style="width:270px;position:relative;top:10px;" disabled="disabled">
                    <select :id="i" style="visibility:hidden">
                        <option v-for="x in health_list" v-if="x==item" selected="selected" :value="x">{{x}}</option>
                        <option  v-for="x in health_list" v-if="x!=item"  :value="x">{{x}}</option>
                    </select>
                </td>

                <td class="b"><button class="handle caozuo" :id="key" @click="edit(key,i)">编&nbsp;辑</button></td>
                <td class="b"><button class="handle caozuo"  @click="del(key,item)">删&nbsp;除</button></td>
            </tr>
            
        </table>
        
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
            customer_list:'',
            old_customer:'',
            old_health:'',
            customer:'',
            health:'',
            health_list:'',
            add_cu:'',
            add_he:'',
            cha_cu:'',
            re_he:'',
        }
    },
    computed:{
        _get:function(){
            this.axios.get('/api/ac_customer/').then((res)=>{
                if(res.data.code==200){
                    this.customer_list=res.data.customer_list
                    this.health_list=res.data.health_list
                    
                }
                })
        }
    },
    methods:{
        edit2:function(){
            if(document.getElementById('bian').innerHTML=='编&nbsp;辑'){
                document.getElementById('ss').removeAttribute('disabled')
                document.getElementById('ss').style.background='white'
                document.getElementById('ss').style.border='1px solid pink'
                document.getElementById('i').removeAttribute('disabled')
                document.getElementById('bian').innerHTML='修&nbsp;改'
                document.getElementById('shan').disabled='disabled'
                this.old_customer=this.cha_cu
                this.old_health=document.getElementById('i').value
            }else{
                this.health=document.getElementById('i').value
                this.axios.post('/api/gai_customer/',
					Qs.stringify({ 
                        old_customer:this.old_customer,
                        customer:document.getElementById('ss').value,
                        health:this.health,
                        old_health:this.old_health
            		}),
					).then((res)=>{
						if(res.data.code==200){
                            alert('修改成功')
                            parent.location.reload()
						}
					})
            }
        },
        cha_re:function(){
            this.cha_cu=document.getElementById('cha_cu').value
            if(this.cha_cu){
                document.getElementById('cha_cu').value=''
                this.axios.post('/api/cha_customer/',
					Qs.stringify({ 
                        customer:this.cha_cu,
            		}),
					).then((res)=>{
						if(res.data.code==200){
                            this.re_he=res.data.health
                            
						}else{
                            this.re_he=''
                            alert('无结果')
                            
                        }
					})
            }else{
                alert('请输入完成参数')
            }
        },
        cha_c:function(){
            document.getElementById('add_cu').value=''
            document.getElementById('all_').style.display='none'
            document.getElementById('cha').style.display='block'
            document.getElementById('add').style.display='none'
        },
        add_c:function(){
            this.re_he=''
            document.getElementById('all_').style.display='none'
            document.getElementById('add').style.display='block'
            document.getElementById('cha').style.display='none'
        },
        add_re:function(){
            this.add_cu=document.getElementById('add_cu').value
            this.add_he=document.getElementById('add_he').value
            if(this.add_cu&&this.add_he){
                this.axios.post('/api/add_customer/',
					Qs.stringify({ 
                        customer:this.add_cu,
                        health:this.add_he,
            		}),
					).then((res)=>{
						if(res.data.code==200){
                            alert('添加成功')
                            parent.location.reload()
						}else{
                            alert('已存在，添加失败')
                        }
					})
            }else{
                alert('请输入完成参数')
            }
        },
        xiugai:function(k,i){
            var r=document.getElementsByClassName(k)
            this.customer=r[0].value
            this.health=document.getElementById(i).value
            this.axios.post('/api/gai_customer/',
					Qs.stringify({ 
                        old_customer:this.old_customer,
                        customer:this.customer,
                        health:this.health,
                        old_health:this.old_health
            		}),
					).then((res)=>{
						if(res.data.code==200){
                            alert('修改成功')
                            parent.location.reload()
						}
					})
        },
        edit:function(k,i){
            if(document.getElementById(k).innerHTML=='编&nbsp;辑'){
                document.getElementById(i).style.visibility='visible'
                var x=document.getElementsByClassName(k)
                this.old_customer=x[0].value
                this.old_health=x[1].value
                x[0].removeAttribute('disabled')
                x[0].style.background='white'
                x[0].style.border='1px solid pink'
                x[1].style.display='none'
                var y=document.getElementsByClassName('caozuo')
                for(var i=0;i<y.length;i++){
                    y[i].disabled='disabled'
                }
                document.getElementById(k).innerHTML='修&nbsp;改'
                document.getElementById(k).removeAttribute('disabled')
            }else{
                this.xiugai(k,i)
            }
        },
        del:function(k,item){
            this.customer=k
            this.health=item
            this.axios.post('/api/del_customer/',
					Qs.stringify({ 
                        customer:this.customer,
                        health:this.health
            		}),
					).then((res)=>{
						if(res.data.code==200){
                            alert('删除成功')
                            parent.location.reload()
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
            location.reload();
        }
    }
}
</script>

<style scoped>
    @import "../../static/css/customer.css"; 
</style>