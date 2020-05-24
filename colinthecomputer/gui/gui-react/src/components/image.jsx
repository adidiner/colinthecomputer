import React, { Component } from 'react';
import Loading from './loading';


class Image extends Component {
  state = {loaded: null, path: null}
  render() {
    if (!this.state.loaded) {
      return (
        <Loading />
        );
    }

    return (
      <img src={window.api_root + this.state.path} width="300"/>
      );
  }

  componentDidMount = () => {
    var user_id = this.props.user_id;
    var snapshot_id = this.props.snapshot_id;
    var type = this.props.type;
    fetch(`${window.api_root}/users/${user_id}/snapshots/${snapshot_id}/${type}`, {
      method: 'GET',
      mode:'cors',
      dataType: 'json'
    })
    .then(response => {
      if (!response.ok) {
        console.log(response);
        throw Error(response.statusText);
      }
      return response;
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      this.setState({loaded: true, 
                    path: data.path});
    })
    .catch(error => {
      console.log(error); // todo
    });
  }
}


export default Image;