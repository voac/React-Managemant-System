import React from 'react';

// React는 하나의 라이브러리이자 클래스이다!
// 기본적으로 제공되는 함수, 안에 그려지는 내용들이 담긴다.
// JSX의 문법 : 두 개 이상의 태그를 사용할 때에는 반드시 <div> 태그를 이용해 하나로 묶어서 사용해야 한다.

class Customer extends React.Component {
    render() {
        return (
            <div>
                <CustomerProfile id = {this.props.id} image = {this.props.image} name = {this.props.name}/>
                <CustomerInfo birthday = {this.props.birthday} gender = {this.props.gender} job = {this.props.job}/>
            </div>
        )
    }
}

class CustomerProfile extends React.Component {
    render() {
        return (
            <div>
                <img src={this.props.image} alt = "profile"/>
                <h2>{this.props.name}({this.props.id})</h2>
            </div>
        )
    }
}

class CustomerInfo extends React.Component {
    render() {
        return (
            <div>
                <p>{this.props.birthday}</p>
                <p>{this.props.gender}</p>
                <p>{this.props.job}</p>
            </div>
        )
    }
}

export default Customer;