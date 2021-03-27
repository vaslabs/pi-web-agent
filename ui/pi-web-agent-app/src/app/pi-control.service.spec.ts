import { TestBed } from '@angular/core/testing';

import { PiControlService } from './pi-control.service';

describe('PiControlService', () => {
  let service: PiControlService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PiControlService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
