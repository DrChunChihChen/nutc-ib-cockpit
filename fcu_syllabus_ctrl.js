//** value 、constant**//
(function () {
    angular.module("Myapp")
           .value("formStatus", { isLoading: false, message: null, modified: false })
}
)();


//FullVersionController
(function () {
    angular.module("Myapp").controller("FullVersionController", fn)

    fn.$inject = ["dataService", "$state", "modal", "formStatus", "$http", "$stateParams", "$translate", "caculateService"]

    function fn(dataService, $state, modal, formStatus, $http, $stateParams, $translate, caculateService) {
        var vm = this;
        var urlParams = new URLSearchParams(window.location.search);
        var access_token = urlParams.get("token");

        vm.params = $stateParams; //處理語系
        $translate.use(vm.params.lang);

        vm.info = [];
        vm.subTitleDesc = [];
        vm.description = [];
        vm.teachersInfo = [];
        vm.gradeRules = [];
        vm.learnHours = [];
        vm.downloadPdf = downloadPdfFn;
        vm.total = totalFn;
        _init();

        function _init() {
            dataService.getCourseDetail(access_token).then(function (result) {
                if (result.success) {
                    vm.info = result.info;
                    vm.subTitleDesc = result.subTitleDesc;
                    vm.description = result.description;
                    vm.targets = result.targets;
                    vm.teachersInfo = result.teachersInfo;
                    vm.textBooks = result.textBooks;
                    vm.readings = result.readings;
                    vm.iSoftwares = result.iSoftwares;
                    vm.assistSoftwares = result.assistSoftwares;
                    vm.weeklyScds = result.weeklyScds;
                    vm.gradeRules = result.gradeRules;
                    vm.gradeRuleDescribe = result.gradeRuleDescribe;
                    vm.integrity = result.integrity;
                    vm.policy = result.policy;
                    vm.courseBankC = result.courseBankC;
                    vm.topicSdgs = result.topicSdgs;
                    vm.topicAiIndicators = result.topicAiIndicators || [];
                    vm.crossVersionYearValue = result.crossVerYear;
                    if (vm.weeklyScds) weeklyTotalFn(); 
                } else {
                    modal.alert({ alertText: $translate.instant('ERROR.GET_COURSEDATA') });
                }
            });
        }

        function downloadPdfFn() {
            dataService.downloadPdf(access_token, vm.params.lang).then(function (result) {
                if (result.success) {
                    if (result.url == "noLogin") {
                        modal.alert({ alertText: $translate.instant('MSG_USE_PDF_BEFORE_LOGIN') });
                    } else {
                        window.open(result.url, '_blank');
                    }
                }
            });
        }

        function totalFn() {
            var total = 0;
            vm.gradeRules.forEach(function (item) {
                total += item.score_rate || 0;
            })

            return total;
        }

        function weeklyTotalFn() {
            var result = caculateService.calculateTotal(vm.weeklyScds);
            vm.learnHours = result.learnHours;
        }

    }
}
)();
