// express 서버에서 JWT 인증 미들웨어, 라우터, 에러 처리 구조 개선
const express = require('express');
const jwt = require('jsonwebtoken');
const { promisify } = require('util');

const app = express();
const PORT = process.env.PORT ?? 3000;
const SECRET_KEY = process.env.SECRET_KEY ?? 'your_secret_key';
const verifyToken = promisify(jwt.verify);

app.use(express.json());

async function authenticateToken(req, res, next) {
    const authHeader = req.headers.authorization;
    const token = authHeader?.split(' ')[1];

    if (!token) {
        return res.status(401).json({ message: 'Access token is missing' });
    }

    try {
        req.user = await verifyToken(token, SECRET_KEY);
        next();
    } catch (err) {
        return res.status(403).json({ message: 'Invalid access token' });
    }
}

function handleLogin(req, res) {
    const { username } = req.body;
    if (!username) {
        return res.status(400).json({ message: 'Username is required' });
    }

    const user = { name: username };
    const accessToken = jwt.sign(user, SECRET_KEY, { expiresIn: '1h' });
    res.json({ accessToken });
}

function handleProtected(req, res) {
    res.json({ message: 'This is a protected route', user: req.user });
}

function handleNotFound(req, res) {
    res.status(404).json({ message: 'Route not found' });
}

function handleError(err, req, res, next) {
    console.error(err.stack);
    res.status(500).json({ message: 'Internal Server Error' });
}

const authRouter = express.Router();
authRouter.post('/login', handleLogin);
authRouter.get('/protected', authenticateToken, handleProtected);

app.use('/api', authRouter);
app.use(handleNotFound);
app.use(handleError);

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});