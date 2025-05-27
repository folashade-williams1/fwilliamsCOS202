import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { NestExpressApplication } from '@nestjs/platform-express';
import { join } from 'path';
import * as nunjucks from 'nunjucks';
async function bootstrap() {
//create a Nest application with Express under the hood
const app = await NestFactory.create<NestExpressApplication>(
AppModule,
);
const express = app.getHttpAdapter().getInstance();

const views = join(__dirname, '..', 'views');
nunjucks.configure(views, { express });
const staticAssets = join(__dirname, '..', 'static');
app.useStaticAssets(staticAssets);

//start the application
await app.listen(3007);
}
bootstrap();