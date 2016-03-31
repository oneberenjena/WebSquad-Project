((function () {

    'use strict';

    /*@ngInject*/
    function DashboardChatBoardCtrl(common, datacontext, ChatService, $mdSidenav) {
        var vm = this,
            $stateParams = common.$stateParams,
            $rootScope = common.$rootScope;

        function activate() {
            vm.selected = ChatService.data.selected;
        }

        function checkProfile(){
            common.$state.go("dashboard.chat.board.profile");
        }
        /*DEFINITION OF VARIABLES*/
        activate();



        function toggleList(){
            $mdSidenav("chats").toggle();
        }

        vm.toggleList = toggleList;

        vm.checkProfile = checkProfile;
    }

    angular.module('hiraApp.dashboard.chat.board')
        .controller('DashboardChatBoardCtrl', DashboardChatBoardCtrl);

})());