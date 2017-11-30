(function() {
    'use strict';

    angular
        .module('app.contacts')
        .controller('ContactsController', ContactsController);

    // 'isLoggedIn' is passed from the config.route.js
    ContactsController.$inject = ['$location', '$localStorage', '$timeout', 'isLoggedIn', 'ContactService', 'UserService', 'notifyService'];

    function ContactsController($location, $localStorage, $timeout, isLoggedIn, ContactService, UserService, notifyService) {
        var vm = this;

        if (!isLoggedIn) {
            $location.path('/');
            return;
        }

        vm.contacts = '';
        vm.username = $localStorage.username;
        vm.deleteContact = deleteContact;
        vm.newContact = newContact;
        vm.updateContact = updateContact;
        vm.copyContact = copyContact;

        vm.new = {
            name: '',
            email:  '',
            phone: '',
            address: ''
        };

        vm.edit = {
            name: '',
            email:  '',
            phone: '',
            address: ''
        };

        contacts();

        ////////////////////
        function contacts() {
            var query = ContactService.contact($localStorage.token).query();
            query.$promise
                .then(function(data) {
                    vm.contacts = data;
                }).catch(function(error) {
                    console.log(error);
                    vm.contacts = error;
                });
        }

        function deleteContact(contact) {
            var i;
            for (i = 0; i < vm.contacts.length; i++)
                if(vm.contacts[i].id === contact.id)
                    break;

            var query = ContactService.contact($localStorage.token).delete({id: contact.id});
            query.$promise
                .then(function(data) {
                    vm.contacts.splice(i, 1);
                }).catch(function(error) {
                    console.log(error);
                });
        }

        function newContact() {
            // TODO: Error checking must have at least 'contact' filled out
            if (vm.new.contact === '')
                return;

            var query = ContactService.contact($localStorage.token).save({
                name: vm.new.name,
                email: vm.new.email,
                phone: vm.new.phone,
                address: vm.new.address
            });

            query.$promise
                .then(function(data) {
                    vm.contacts.unshift(data);
                    $('#newContactModal').modal('hide');
                    notifyService.display('Added New Contact');
                    $timeout(function() {
                        notifyService.showMessage = false;
                    }, 3000);
                })
                .catch(function(error) {
                    console.log(error);
                });
        }

        function updateContact() {
            var i;
            for(i = 0; i < vm.contacts.length; i++)
                if (vm.contacts[i].id === vm.edit.id)
                    break;
            // No reason to send update request if objects are still the same
            if (angular.equals(vm.contacts[i], vm.edit))
                return;

            var query = ContactService.contact($localStorage.token).update({id: vm.edit.id}, {
                name: vm.edit.name,
                email: vm.edit.email,
                phone: vm.edit.phone,
                address: vm.edit.address
            });

            query.$promise
                .then(function(response) {
                    vm.contacts[i] = vm.edit;
                    $('#updateContactModal').modal('hide');
                    notifyService.display('Updated Contact');
                    $timeout(function() {
                        notifyService.showMessage = false;
                    }, 3000);
                })
                .catch(function(error) {
                    console.log(error);
                });
        }

        function copyContact(contact) {
            vm.edit = angular.copy(contact);
        }
    }
})();
