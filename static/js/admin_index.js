/**
 * Created by RaPoSpectre on 11/8/16.
 */

Vue.config.delimiters = ['${', '}}'];
var vm = new Vue({
    el: '#vCollections',
    data: {},
    methods: {
        getData: function (page) {
            var url = generateUrl('super/admin/api/site/overview') + '&page=' + page;
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('sites', data.body.site_list);
                    this.$set('pageObj', data.body.page_obj);
                }
            });
        },
        initSiteData: function (slug) {
            var url = generateUrl('super/admin/api/task/') + '&slug=' + slug;
            this.$http.get(url, function (data) {
                if(data.status == 1){
                    $.scojs_message('任务提交成功', $.scojs_message.TYPE_OK);
                    this.getData(1);
                }else{
                    $.scojs_message(data.msg, $.scojs_message.TYPE_ERROR);
                }
            })
        }


    },
    ready: function () {
        this.getData(1);
    },
    computed: {
        noData: function () {
            return this.sites == null;
        }
    }
});
