((function () {
    'use strict';

    function model() {
        var service = {};

        /*DEFINITION OF VARIABLES*/

        var repos = {
            users: {
                entity: 'users'
            },
            chats: {
                entity: 'chats'
            },
            contacts: {
                entity: 'contacts'
            },
            groups: {
                entity: 'groups'
            },
            memberships: {
                entity: 'memberships'
            },
            pages: {
                entity: 'pages'
            }
        };

        var defaultCols = [
            {
                name: 'ID',
                attr: '_id'
            },
            {
                name: 'Nombre',
                attr: 'name'
            }
        ];

        var adminCols = {
            views: [
                {
                    name: 'Parent',
                    attr: 'parent'
                },
                {
                    name: 'Level',
                    attr: 'level'
                }
            ],
            blocks: [
                {
                    name: 'Title',
                    attr: 'title'
                },
                {
                    name: 'View',
                    attr: 'view'
                }
            ]
        };

        /*PUBLIC FUNCTIONS*/
        service.repos = repos;

        service.columns = function (collection) {
            var cols = [];
            var adminAllowed = adminCols[collection];
            var i, j;

            for (i = 0; i < defaultCols.length; i += 1) {
                cols.push(defaultCols[i]);
            }

            if (adminAllowed) {
                for (j = 0; j < adminCols[collection].length; j += 1) {
                    cols.push(adminCols[collection][j]);
                }
            }

            return cols;
        };

        return service;
    }

    angular
        .module('hiraApp.data')
        .factory('model', model);
})());