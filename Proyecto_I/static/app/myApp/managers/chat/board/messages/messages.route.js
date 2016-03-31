((function() {
    'use strict';

    function getStates() {
        return [{
            name: 'dashboard.chat.board.messages',
            config: {
                views: {
                    '@dashboard.chat': {
                        templateUrl: 'app/myApp/managers/chat/board/messages/messages.html',
                        controller: 'DashboardChatMessagesCtrl',
                        controllerAs: 'vm'
                    },
                    'textBox@dashboard.chat.board.messages':{
                        templateUrl: 'app/myApp/managers/chat/board/messages/textBox/textBox.html',
                        controller: 'DashboardChatMessagesTextBoxCtrl',
                        controllerAs: 'vm'
                    }
                }
            }
        }];
    }

    /* @ngInject */
    function stateConfig(statehelper) {
        statehelper.configureStates(getStates());
    }

    angular
        .module('hiraApp.dashboard.chat.messages')
        .run(stateConfig);

})());
