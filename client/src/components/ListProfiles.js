import React, { Component } from 'react';
import { graphql } from 'react-apollo'; // what actually binds react to apollo
import { getProfilesQuery } from '../queries/queries'
import { DisplayProfile } from './DisplayProfile'

class ListProfiles extends Component {
  state = {
    displayCount: 10,
    profiles: []
  }

  loadMore  = () =>{
    console.log("load more")
    let newDisplayCount = this.state.displayCount;
    newDisplayCount += 10
    let data = this.props.data;
    let newProfiles = data.profiles.slice(0, this.state.displayCount)

    this.setState({
      displayCount: newDisplayCount
    })

    this.setState ({
      profiles: newProfiles
    })
  }

  displayProfiles() {

    let data = this.props.data


    //check to see if query is still loading, otherwise display books names in list
    if(data.loading) {
      return <div>Loading profiles...</div>
    } else {
      return data.profiles.map(profile => (
        
          <div>
            {profile.name}
            <DisplayProfile props={profile} ></DisplayProfile>

          </div>

        )
      )
    }
  }

  render() {
    console.log(this.props);
    console.log(this.state);
    return (
      <div>
        <div id="book-list" >
          { this.state.profiles.map(profile => (
            <div>
              <DisplayProfile props={profile}></DisplayProfile>
            </div>
          ))}
        </div>
        <button onClick={this.loadMore}>
        Load More
        </button>

        { this.displayProfiles() }
      </div>
    );
  }
}


// below we are taking the "getBooksQuery" query and binding it to the BookList component
// it stores the query information in the components props

export default graphql(getProfilesQuery)(ListProfiles);
