function [roi, halo] = makeCellposeRois(filepath, watershed_width, halo_multiplier, show_plot)
% lloyd russell 2020
% written as almost drop in replacment for 'dilateCentroids' simplePipeline function
% for subsequent use with extractTraces function

% inputs:
% filepath = path to .MAT file from cellposeForNaparm
% watershed_width = pixels to exclude around each roi before making halo mask
% halo_multiplier = (multiplier of roi diameter) sigma for gaussian function around each roi
% show_plot = display the roi masks

% output
% roi - num_planes cell array. each cell is an array of structs where each element is an ROI with the following fields: coords (linear xy coords to index into image/movie), weights, image(of the mask)
% halo - same as roi but for halo (neuropil) masks


load(filepath)  % loads cellpose masks

nplanes = size(masks,1);
all_rois = [];
all_halos = [];

if show_plot
    figure
end

for p = 1:nplanes
    masks_p = double(squeeze(masks(p,:,:)));
    
    maskImg2 = zeros(size(masks_p));
    maskCoords = [];
    maskCentroids = [];
    numFound = max(masks_p(:));
    all_rois{p} = [];
    all_halos{p} = [];
    for m = 1:numFound
        % fill in small holes in the roi masks
        tempImg = imfill(masks_p==m, 'holes');
        
        % keep the roi mask image
        all_rois{p}(:,:,m) = tempImg;
        
        tempInd = find(tempImg);
        [tempIndY, tempIndX] = ind2sub(size(masks_p), tempInd);
        maskCoords{m} = [tempIndX tempIndY];
        maskCentroids(m,:) = round(median(maskCoords{m}));
        
        % colour in pixel in new mask image
        maskImg2(tempInd) = m;
    end
    
    % get average roi diamter, to use for halo generation
    maskCoord_min = cellfun(@min, maskCoords', 'UniformOutput',0);
    maskCoord_min = cell2mat(maskCoord_min);
    maskCoord_max = cellfun(@max, maskCoords', 'UniformOutput',0);
    maskCoord_max = cell2mat(maskCoord_max);
    maskCoord_dif = maskCoord_max - maskCoord_min;
    meanROIdiam = round(mean(mean(maskCoord_dif)));
    halo_mask = fspecial('gaussian', meanROIdiam*halo_multiplier*6, meanROIdiam*halo_multiplier);
    halo_mask = halo_mask./max(max(halo_mask));
    
    % exclude a safe buffer region around all ROIs
    allMasks = maskImg2>0;
    allMasksWatershed = imdilate(allMasks, strel('disk',watershed_width,8));
    
    % make halo (neuropil) maks for each ROI
    for m = 1:numFound
        blankImg = zeros(size(masks_p));
        blankImg(maskCentroids(m,2), maskCentroids(m,1)) = 1;
        
        temp = conv2(blankImg, halo_mask, 'same');
        temp(allMasksWatershed) = 0;
        temp = temp ./ nanmax(temp(:));
        all_halos{p}(:,:,m) = temp;
    end
    
    

    % plot the results
    if show_plot
        max_roi = max(all_rois{p},[],3);
        max_halo = max(all_halos{p},[],3);
        subplot(2,2,p)
        fov_im = double(squeeze(img(p,:,:)));
        fov_im = fov_im ./ max(fov_im(:));
        roi_im = max_roi + (max_halo/2);
        imagesc([fov_im roi_im]);
        axis equal; axis off; drawnow
        title(['Plane ' num2str(p)])
    end
    
    
    % save the results
    roi{p} = cell(numFound,1);
    halo{p} = cell(numFound,1);
    for i = 1:numFound
        % roi
        [coords_y, coords_x, weights] = find(all_rois{p}(:,:,i) > 0);
        roi{p}{i}.coords = sub2ind(size(masks_p), coords_y, coords_x);
        roi{p}{i}.weights = weights;
        roi{p}{i}.image = all_rois{p}(:,:,i);
        
        % halo
        [coords_y, coords_x, weights] = find(all_halos{p}(:,:,i) > 0.05);
        halo{p}{i}.coords = sub2ind(size(masks_p), coords_y, coords_x);
        halo{p}{i}.weights = weights;
        halo{p}{i}.image = all_halos{p}(:,:,i);
    end
end
