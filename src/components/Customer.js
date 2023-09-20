import React from 'react';

class Customer extends React.Component { // React는 하나의 라이브러리이자 클래스이다!
    render() { // 기본적으로 제공되는 함수, 안에 그려지는 내용들이 담긴다.
        return (
            <div>
                <h2>{this.props.name}</h2>
                <p>{this.props.birthday}</p>
                <p>{this.props.gender}</p>
                <p>{this.props.job}</p>
            </div>
        )
    }
}

export default Customer;