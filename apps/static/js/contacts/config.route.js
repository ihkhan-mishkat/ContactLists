(function() {
    'use strict';

    angular
        .module('app.contacts')
        .config(configFunction);

    configFunction.$inject = ['$routeProvider', 'STATIC_URL'];

    function configFunction($routeProvider, STATIC_URL) {
        $routeProvider.when('/contacts', {
            templateUrl: STATIC_URL + '/contacts/contacts.html',
            controller: 'ContactsController',
            controllerAs: 'vm',
            resolve: {isLoggedIn: resolveUser}
        });
    }

    resolveUser.$inject = ['authService'];

    function resolveUser(authService) {
        return authService.isLoggedIn();
    }
})();
