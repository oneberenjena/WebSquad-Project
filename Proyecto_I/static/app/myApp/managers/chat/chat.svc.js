((function () {
    'use strict';

    /*@ngInject*/
    function ChatService(datacontext) {
        var PublicAPI = {},
            data = {
                contacts: [],
                chats : [],
                selected: {},
                show: {
                    contacts: false
                }
            };

        function setChats(cb){
            var options = {
                forceRemote: false,
                manager: 'chats'
            };

            datacontext.chats.list(options).then(function(res){
                data.chats = res;
                cb(true);
            });
        }

/*        function setContacts(cb){
            var options = {
                forceRemote: false,
                manager: 'contacts'
            };

            datacontext.contacts.list(options).then(function(res){
                data.contacts = res;
                cb(true);
            });
        }*/

        function selectChat(chat){
            angular.copy(chat,data.selected);
        }

        function getChats(){
            return data.chats;
        }

        function showChats(){
            data.show.contacts = false;
        }

        function showContacts(){
            data.show.contacts = true;
        }

        PublicAPI.setChats = setChats;
        PublicAPI.data = data;
        PublicAPI.selectChat = selectChat;
        PublicAPI.showChats = showChats;
        PublicAPI.showContacts = showContacts;

        return PublicAPI;
    }

    angular
        .module('hiraApp.dashboard.chat')
        .factory('ChatService', ChatService);

})());