import React, { Component } from 'react';
import NewUser from './NewUser';
import EditUser from './EditUser';
import EnhancedTable from '../Table'
import PropTypes from 'prop-types';
import { withSnackbar } from 'notistack';
import AuthService from '../../AuthService';

class Users extends Component {
  Auth = new AuthService();

  constructor(props) {
    super(props);
    this.props.Collapse("users")
    
  }

  state = {
    newForm: false,
    EditForm: false,
    data: [],
    selected: [],
    selectedUser: [],
  };

  componentDidMount() {
    this.getUsersFromBackend();
  }

  getUsersFromBackend = () => {
    this.Auth.fetch(window.USER_GET).then(
      function (result) {
        this.setState({ data: result.response })
      }.bind(this)
    ).catch(err => {
      alert(err);
    })
    this.setState({ selected: [] });
  }

  handleDelete = () => {
    var options = {
      'method': 'DELETE',
      'body': JSON.stringify({ id: this.state.selected })
    }
    this.Auth.fetch(window.USER_DELETE, options).then(
      function (result) {
        this.getUsersFromBackend();
        this.handleNotification("User has been deleted", 'warning')
      }.bind(this)
    ).catch(err => {
      alert(err);
    })

  }

  handleFormOpen = form => {
    this.setState({
      [form]: true,
    });
  };

  handleFormClose = form => {
    this.setState({
      [form]: false,
    });
  };
  updatedSelected = (value, row) => {
    this.setState({ selected: value });
    if (value.length === 1) {
      this.setState({ selectedUser: row[value] });
    }
  }
  handleNotification = (message, variant) => {
    // variant could be success, error, warning or info
    this.props.enqueueSnackbar(message, { variant });
  };

  render() {
    const fields = [
      { id: 'id', align: 'left', disablePadding: true, label: 'ID' },
      { id: 'email', align: 'left', disablePadding: false, label: 'Username' },
      { id: 'role', align: 'left', disablePadding: false, label: 'Role' },
    ];

    return (
      <div>
        <EnhancedTable
          data={this.state.data}
          fields={fields}
          selected={this.state.selected}
          handleFormOpen={this.handleFormOpen}
          handleDelete={this.handleDelete}
          updatedSelected={this.updatedSelected}
          title="User Administration"
          rowsPerPage={5}
        />
        <NewUser
          open={this.state.newForm}
          Auth={this.Auth}
          handleFormClose={this.handleFormClose}
          getUsersFromBackend={this.getUsersFromBackend}
          notification={this.handleNotification}
        />
        <EditUser
          open={this.state.EditForm}
          Auth={this.Auth}
          handleFormClose={this.handleFormClose}
          user={this.state.selectedUser}
          getUsersFromBackend={this.getUsersFromBackend}
          notification={this.handleNotification} />
      </div>

    )
  }
}
Users.propTypes = {
  enqueueSnackbar: PropTypes.func.isRequired,
};

export default withSnackbar(Users);