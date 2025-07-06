import React, { useState, useEffect } from 'react';
import { initializeApp } from 'firebase/app';
import {
  getFirestore,
  collection,
  getDocs,
  addDoc,
  deleteDoc,
  doc,
} from 'firebase/firestore';

const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_AUTH_DOMAIN",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_STORAGE_BUCKET",
  messagingSenderId: "YOUR_MSG_ID",
  appId: "YOUR_APP_ID"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

export default function Home() {
  const [lang, setLang] = useState('uz');
  const [products, setProducts] = useState([]);
  const [newProduct, setNewProduct] = useState({ name: '', price: '', image: '' });

  const t = {
    uz: {
      title: "Arzon Tavarlar",
      welcome: "Xush kelibsiz! Arzon va sifatli mahsulotlar bu yerda.",
      addToCart: "Savatga qo‘shish",
      price: "Narxi",
      buy: "Sotib olish",
      langBtn: "Русский",
      addProduct: "Mahsulot qo‘shish",
      name: "Nomi",
      img: "Rasm URL",
    },
    ru: {
      title: "Дешевые Товары",
      welcome: "Добро пожаловать! Здесь дешевые и качественные товары.",
      addToCart: "Добавить в корзину",
      price: "Цена",
      buy: "Купить",
      langBtn: "O‘zbekcha",
      addProduct: "Добавить товар",
      name: "Название",
      img: "Ссылка на изображение",
    },
  };

  const fetchProducts = async () => {
    const querySnapshot = await getDocs(collection(db, 'products'));
    const items = [];
    querySnapshot.forEach((doc) => {
      items.push({ id: doc.id, ...doc.data() });
    });
    setProducts(items);
  };

  const addProduct = async () => {
    if (!newProduct.name || !newProduct.price || !newProduct.image) return;
    await addDoc(collection(db, 'products'), newProduct);
    setNewProduct({ name: '', price: '', image: '' });
    fetchProducts();
  };

  const deleteProduct = async (id) => {
    await deleteDoc(doc(db, 'products', id));
    fetchProducts();
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  return (
    <div className="p-4 max-w-3xl mx-auto">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-3xl font-bold">{t[lang].title}</h1>
        <button
          onClick={() => setLang(lang === 'uz' ? 'ru' : 'uz')}
          className="bg-gray-200 px-3 py-1 rounded"
        >
          {t[lang].langBtn}
        </button>
      </div>

      <p className="mb-6">{t[lang].welcome}</p>

      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-2">{t[lang].addProduct}</h2>
        <input
          className="border p-1 mr-2"
          type="text"
          placeholder={t[lang].name}
          value={newProduct.name}
          onChange={(e) => setNewProduct({ ...newProduct, name: e.target.value })}
        />
        <input
          className="border p-1 mr-2"
          type="text"
          placeholder="Narxi / Цена"
          value={newProduct.price}
          onChange={(e) => setNewProduct({ ...newProduct, price: e.target.value })}
        />
        <input
          className="border p-1 mr-2"
          type="text"
          placeholder={t[lang].img}
          value={newProduct.image}
          onChange={(e) => setNewProduct({ ...newProduct, image: e.target.value })}
        />
        <button onClick={addProduct} className="bg-green-600 text-white px-3 py-1 rounded">+</button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {products.map((item) => (
          <div key={item.id} className="border p-4 rounded-xl shadow">
            <img
              src={item.image}
              alt="Tovar rasmi"
              className="w-full h-48 object-cover mb-2 rounded"
            />
            <h2 className="text-xl font-semibold">{item.name}</h2>
            <p className="text-sm text-gray-600">{t[lang].price}: {item.price}</p>
            <button className="bg-blue-600 text-white mt-2 px-4 py-1 rounded">
              {t[lang].addToCart}
            </button>
            <button onClick={() => deleteProduct(item.id)} className="text-red-600 text-xs mt-1 block">O‘chirish</button>
          </div>
        ))}
      </div>
    </div>
  );
}
