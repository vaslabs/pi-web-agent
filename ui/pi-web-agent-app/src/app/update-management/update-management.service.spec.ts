import { TestBed } from '@angular/core/testing';

import { UpdateManagementService } from './update-management.service';

describe('UpdateManagementService', () => {
  let service: UpdateManagementService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(UpdateManagementService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
