import AuthService from '../../AuthService';

export default class ActionService {
    constructor() {
        this.Auth = new AuthService();
    }

    getData() {
        return new Promise((resolve, reject) => {
            this.Auth.fetch(window.DEVICE_GET)
                .then(result => {
                    resolve(result.response);
                })
                .catch(err => {
                    reject(String(err).replace(/Error:/g, ''));
                });
        });
    }
    getDataWithTimeOut() {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                this.Auth.fetch(window.DEVICE_GET)
                    .then(result => {
                        resolve(result.response);
                    })
                    .catch(err => {
                        reject(String(err).replace(/Error:/g, ''));
                    });
            }, 2000);
        });
    }
    addDevice(state, fields) {
        var json = {};
        json.id = state.lastSelectedRow.id;

        fields
            .filter(field => {
                return field.addForm;
            })
            .map(field => {
                return (json[field.id] = state[field.id]);
            });
        return new Promise((resolve, reject) => {
            if (Object.keys(json).length > 1) {
                console.log(json);
                var options = {
                    method: 'POST',
                    body: JSON.stringify(json)
                };
                this.Auth.fetch(window.DEVICE_ADD, options)
                    .then(result => resolve(result.response))
                    .catch(err => {
                        reject(String(err).replace(/Error:/g, ''));
                    });
            } else {
                reject('User not created');
            }
        });
    }
    deleteDevice(selected) {
        return new Promise((resolve, reject) => {
            var options = {
                method: 'DELETE',
                body: JSON.stringify({ id: selected })
            };
            this.Auth.fetch(window.DEVICE_DELETE, options)
                .then(result => resolve(result.response))
                .catch(err => {
                    reject(String(err).replace(/Error:/g, ''));
                });
        });
    }

    editDevice(state, fields) {
        var json = {};
        json.id = state.lastSelectedRow.id;

        fields
            .filter(field => {
                return field.editForm;
            })
            .map(field => {
                let changed = field.id + '_changed';
                if (state[changed]) {
                    json[field.id] = state[field.id];
                }
                return json;
            });
        return new Promise((resolve, reject) => {
            if (Object.keys(json).length > 1) {
                console.log(json);
                var options = {
                    method: 'PUT',
                    body: JSON.stringify(json)
                };
                this.Auth.fetch(window.DEVICE_EDIT, options)
                    .then(result => resolve(result.response))
                    .catch(err => {
                        reject(String(err).replace(/Error:/g, ''));
                    });
            } else {
                reject('Device not changed');
            }
        });
    }
}