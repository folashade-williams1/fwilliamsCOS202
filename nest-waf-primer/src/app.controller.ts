import { Controller, Get, Render} from '@nestjs/common';
import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get('hello')
  getHello(): string {
    return this.appService.getHello();
  }

  @Get('hello2')
  @Get('index.html')
  getHello2(): {} {
    return this.appService.getHello2();
  }
  @Get()
  @Render('home.html')
  getHome(): {} {
  return this.appService.getHome();
}
 @Get('about-us')
 @Render('about-us.html')
 getAboutUs(): {} {
  return this.appService.getAboutUs();
}

}
