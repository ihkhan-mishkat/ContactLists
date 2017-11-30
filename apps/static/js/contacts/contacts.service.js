(function() {
    'use strict';

    var app = angular.module('app.contacts');

    app.factory('ContactService', ContactService);
    app.factory('UserService', UserService);

    ContactService.$inject = ['$resource'];
    function ContactService($resource) {
        return {
            contact: function(token) {
                return $resource('/api/contacts/:id/', null, {
                    query: {
                        method: 'GET',
                        isArray: true,
                        headers: {
                            'Authorization': 'Token ' + token
                        }
                    },
                    save: {
                        method: 'POST',
                        isArray: false,
                        headers: {
                            'Authorization': 'Token ' + token
                        }
                    },
                    delete: {
                        method: 'DELETE',
                        isArray: false,
                        headers: {
                            'Authorization': 'Token ' + token
                        }
                    },
                    update: {
                        method: 'PATCH',
                        isArray: false,
                        headers: {
                            'Authorization': 'Token ' + token
                        }
                    }
                });
            }
        };
    }

    UserService.$inject = ['$resource'];
    function UserService($resource) {
        return $resource('/api/users/:id/');
    }
})();
