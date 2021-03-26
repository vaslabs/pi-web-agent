import { TestBed } from '@angular/core/testing';

import { WebsocketServiceService } from './websocket-service.service';

describe('WebsocketServiceService', () => {
  let service: WebsocketServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(WebsocketServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
