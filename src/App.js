import React from 'react';
import Customer from './components/Customer'
import './App.css';


const customers = [
  {
  'id': 1,
  'image': 'https://random.imagecdn.app/64/64',
  'name': '홍길동',
  'birthday': '961122',
  'gender': '남자',
  'job': '대학생'
  },
  {
    'id': 2,
    'image': 'https://random.imagecdn.app/64/64',
    'name': '장현빈',
    'birthday': '061123',
    'gender': '남자',
    'job': '고등학생'
  },
  {
    'id': 3,
    'image': 'https://random.imagecdn.app/64/64',
    'name': '응애',
    'birthday': '061111',
    'gender': '남자',
    'job': '배우'
  }
]

function App() {
  return (
    <div>
      // map을 사용할 땐 key 라는 이름의 props를 사용하자.
      { customers.map(c => { return <Customer key = {c.id} id = {c.id} image = {c.image} name = {c.name} birthday = {c.birthday} gender = {c.gender} job = {c.job} /> }) }
    </div>
  );
}

export default App;
