import { Hono } from 'hono';
import { Context } from 'hono';


// This ensures c.env.DB is correctly typed
type Bindings = {
	DB: D1Database
}

const app = new Hono<{ Bindings: Bindings }>()
app.get('/', (c) => c.text('Hello this is the Webhallen API!'));

app.get('/api/webhallen/products/:product_id', async (c, env) => {
	const product_id = c.req.param('product_id')

	try {
		let { results } = await c.env.DB.prepare("SELECT * FROM Products WHERE id = ?").bind(product_id).all()
		console.log(results);
		return c.json(results)
	} catch (e) {
		console.log(e);
		return c.json({ err: e }, 500)
	}
})


export default app;
