import React, { Component } from 'react';
import { graphql } from 'react-apollo'; // what actually binds react to apollo
import { getProfilesQuery } from '../queries/queries'

class ListProfiles extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selected: null
    }
  }

  displayProfiles() {
    let data = this.props.data

    //check to see if query is still loading, otherwise display books names in list
    if(data.loading) {
      return <div>Loading profiles...</div>
    } else {
      return data.profiles.map(profile => (
          <div>
            <div key={profile.id}>{profile.name}</div>
            <img src={profile.image_url}></img>
          </div>

        )
      )
    }
  }

  render() {
    console.log(this.props);
    return (
      <div>
        <div id="book-list" >
          { this.displayProfiles() }
        </div>
      </div>
    );
  }
}


// below we are taking the "getBooksQuery" query and binding it to the BookList component
// it stores the query information in the components props
export default graphql(getProfilesQuery)(ListProfiles);
