(function () {
    angular.module('Myapp', ['fcu.ui.bootstrap', 'fcumodule', 'ui.router', 'pascalprecht.translate', 'ui.bootstrap', 'ngSanitize', 'caculateWeeklyscd'])
    .config(configFn)

    configFn.$inject = ['$stateProvider', '$urlRouterProvider', '$translateProvider', '$httpProvider','chtlang', 'enlang',]

    function configFn($stateProvider, $urlRouterProvider, $translateProvider, $httpProvider, chtlang, enlang) {
        $httpProvider.defaults.headers.post = {};
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/json; charset=utf-8';

        $translateProvider
            .useSanitizeValueStrategy('sce')
            .translations("cht", chtlang)
            .translations("en", enlang)
            .preferredLanguage("cht")

        $urlRouterProvider
            .otherwise("/fullVer/cht")

        $stateProvider
            .state("fullVer",
                    {
                        url: "/fullVer/:lang",
                        templateUrl: "view/W320104_FullVersion.html?20260825",
                        controller: "FullVersionController",
                        controllerAs: "fullVerCtrl"
                    })
    }

    //htmlViewer
    (function (app, component) {
        angular.module(app)
        .component(component, {
            controller: ControllerFn,
            controllerAs: "vm",
            bindings: {
                data: "<"
            },
            template: '<div ng-bind-html = "vm.html"></div>'
        });
        ControllerFn.$inject = ["$sce"];
        function ControllerFn($sce) {
            var vm = this;
            vm.$onChanges = change;

            function change(changes) {
                if (changes.data) {
                    vm.html = $sce.trustAsHtml(vm.data);
                }
            }

        }

    })("Myapp", "htmlViewer")
}
)();


//Service
(function () {
    angular.module("Myapp")
           .factory("dataService", fn)

    fn.$inject = ["webService"];

    function fn(webService) {

        var service = [];

        service.getCourseDetail = getCourseDetailFn;
        service.downloadPdf = downloadPdfFn;

        return service;
        
        function getCourseDetailFn(access_token) {
            var serviceUrl = "./W320104_syllabus.aspx/GetCourseDetail";
            var params = { access_token: access_token };
            return webService.post(serviceUrl, params).then(function (result) { return result; }, function (error) {
                   return error;
               })
        }

        function downloadPdfFn(access_token, lang) {
            var serviceUrl = "./W320104_syllabus.aspx/DownloadPdf";
            var params = { access_token: access_token, lang: lang };
            return webService.post(serviceUrl, params).then(function (result) { return result; }, function (error) {
                return error;
            })
        }
    }

}
)();





