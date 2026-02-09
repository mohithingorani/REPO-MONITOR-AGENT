import Fastify, {FastifyInstance} from "fastify"

const app : FastifyInstance = Fastify({
    logger:true,
});

const PORT = Number(process.env.PORT)  || 3000

const start = async()=>{
    try{
        await app.listen({port:PORT});
        console.log(`Server running at port : ${PORT}`);
    }catch(err){
        app.log.error(err);
        process.exit(1);
    }
};

start();