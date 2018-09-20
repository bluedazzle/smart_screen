/**
 * Created by rapospectre on 2018/9/18.
 */

Vue.config.delimiters = ['${', '}}'];
var vm = new Vue({
    el: '#vTasks',
    data: {
        tasks: null,
        first: true
    },
    methods: {
        cancelTask: function (task_id) {
            var url = generateUrl('super/admin/api/task/cancel/') + '&id=' + task_id;
            this.$http.get(url, function (data) {
                if(data.status == 1){
                    $.scojs_message('任务终止成功', $.scojs_message.TYPE_OK);
                }else{
                    $.scojs_message(data.msg, $.scojs_message.TYPE_ERROR);
                }
            });
            this.getData(1);
        },
        getData: function (page) {
            var url = generateUrl('super/admin/api/tasks/') + '&page=' + page;
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('tasks', data.body.task_list);
                    this.$set('pageObj', data.body.page_obj);
                    var context = this;
                    this.$nextTick(function () {
                        data.body.task_list.map(function (task) {
                            if(task.status != 3 || context.first){
                                $('#px' + task.id).progress();
                            }
                        });
                        if(context.first){
                           context.first = false;
                        }
                        // $('.progress').progress();
                    })
                }
            });
            var that = this;
            this.timeOut = setTimeout(() => {
                that.getData(page);
                }, 5000);
        },
    },
    created: function () {
        if (this.timeOut) {
            clearTimeout(this.timeOut);
        }
        this.getData(1);
    },
    ready: function () {

    },
    computed: {
        noData: function () {
            return this.tasks == null;
        }
    }
});


