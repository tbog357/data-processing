const { MongoClient } = require("mongodb");

async function main() {
  uri = process.env.MONGODB_URI;
  const client = new MongoClient(uri);
  try {
    await client.connect();

    await generateSampleData(client);
  } catch (err) {
    console.error(err);
  } finally {
    await client.close();
  }
}

main().catch(console.error);

async function generateSampleData(client) {
  while (true) {
    const result = await client.db("ecommerce").collection("listings").insertOne({
      name: "testing",
    });
    console.log(result.insertedId);
  }
}
